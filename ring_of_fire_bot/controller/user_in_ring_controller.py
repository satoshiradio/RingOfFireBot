import json

from sqlalchemy.exc import NoResultFound
from telegram import ParseMode, Update
from telegram.ext import Updater, ConversationHandler, CommandHandler, CallbackContext

from ring_of_fire_bot.model.channel_status import CHANNEL_STATUS
from ring_of_fire_bot.repository.i_unit_of_work import IUnitOfWork
from ring_of_fire_bot.view.error_view import ErrorView
from ring_of_fire_bot.view.ring_view import RingView


class UserInRingController:
    def __init__(self, updater: Updater, unit_of_work: IUnitOfWork):
        self.updater = updater
        self.unit_of_work = unit_of_work
        self.ring_view: RingView = RingView(self.updater)
        self.error_view: ErrorView = ErrorView(self.updater)

    def get_commands(self):
        return ConversationHandler(entry_points=[
            CommandHandler("set_channel_status", self.set_channel_status_command),
            CommandHandler("set_funded", self.set_funded_command)
        ],
            states={}, fallbacks=[], allow_reentry=True)

    def callbacks(self, update: Update, context: CallbackContext):
        callback_function = json.loads(update.callback_query.data)['f']
        if callback_function == 'c':
            self.set_channel_status_callback(update, context)
            return
        if callback_function == 'f':
            self.set_funded_callback(update, context)
            return

    def set_funded_command(self, update: Update, context: CallbackContext):
        chat_id = update.effective_chat.id
        try:
            ring = self.unit_of_work.ring_repository.get_ring(update.message.text, chat_id)
        except NoResultFound:
            self.error_view.ring_not_found(chat_id)
            return
        self.ring_view.set_funded(chat_id, ring.ring_id, update.effective_user.id)

    def set_channel_status_callback(self, update: Update, context: CallbackContext):
        chat_id: int = update.effective_chat.id
        # get data from response
        json_data = json.loads(update.callback_query.data)
        ring_id = json_data['r']
        user_id = json_data['u']
        status = CHANNEL_STATUS[json_data['s']]
        # if other user presses button ignore
        if update.callback_query.from_user.id != user_id:
            return
        # find ring from callback data
        try:
            ring = self.unit_of_work.ring_repository.get(ring_id)
        except NoResultFound:
            self.error_view.ring_not_found(chat_id)
            return
        # find user
        try:
            user = self.unit_of_work.user_repository.get(user_id)
        except NoResultFound:
            self.error_view.not_registered(chat_id)
            return
        # find user in ring
        try:
            user_in_ring = self.unit_of_work.user_in_ring_repository.find_user_in_ring(ring, user)
        except NoResultFound:
            self.error_view.ring_not_found(chat_id)
            return
        # update user in ring
        user_in_ring.channel_status = status
        self.unit_of_work.complete()
        # inform user
        update.callback_query.edit_message_text(
            f"Set channel status to {status.value}",
            parse_mode=ParseMode.HTML)

    def set_channel_status_command(self, update: Update, context: CallbackContext):
        chat_id = update.effective_chat.id
        try:
            ring = self.unit_of_work.ring_repository.get_ring(update.message.text, chat_id)
        except NoResultFound:
            self.error_view.ring_not_found(update.effective_chat.id)
            return
        self.ring_view.set_channel_status(chat_id, ring.ring_id, update.effective_user.id)

    def set_funded_callback(self, update: Update, context: CallbackContext):
        json_data = json.loads(update.callback_query.data)
        ring_id: int = json_data['r']
        user_id: int = json_data['u']
        funded: bool = json_data['s']
        if update.callback_query.from_user.id != user_id:
            return
        try:
            ring = self.unit_of_work.ring_repository.get(ring_id)
        except NoResultFound:
            self.error_view.ring_not_found(update.effective_chat.id)
            return
        user = self.unit_of_work.user_repository.get(user_id)

        user_in_ring = self.unit_of_work.user_in_ring_repository.find_user_in_ring(ring, user)
        user_in_ring.is_funded = funded
        self.unit_of_work.complete()
        update.callback_query.edit_message_text(
            f"Set funded status to {user_in_ring.is_funded}",
            parse_mode=ParseMode.HTML)

