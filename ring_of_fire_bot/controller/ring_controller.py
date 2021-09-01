import json

from sqlalchemy.exc import NoResultFound
from telegram import Update, ParseMode
from telegram.ext import CallbackContext, Updater, ConversationHandler, CommandHandler

from ring_of_fire_bot.model.Exceptions.invalid_node_key_exception import InvalidNodeKeyException
from ring_of_fire_bot.model.ring import Ring
from ring_of_fire_bot.model.ring_status import RING_STATUS
from ring_of_fire_bot.repository.i_unit_of_work import IUnitOfWork
from ring_of_fire_bot.view.error_view import ErrorView
from ring_of_fire_bot.view.ring_view import RingView, detail_ring


class RingController:
    def __init__(self, updater: Updater, unit_of_work: IUnitOfWork):
        self.updater = updater
        self.unit_of_work = unit_of_work
        self.ring_view: RingView = RingView(self.updater)
        self.error_view: ErrorView = ErrorView(self.updater)

    def get_commands(self):
        return ConversationHandler(
            entry_points=[
                CommandHandler("new_ring", self.new_ring),
                CommandHandler("my_rings_as_manager", self.list_rings_of_sender),
                CommandHandler("ring_info", self.get_ring_info),
                CommandHandler("join", self.join_ring),
                CommandHandler("leave", self.leave_ring),
                CommandHandler("ring_status", self.set_ring_status_command),  # manager
                CommandHandler("set_chat", self.set_chat_id),  # manager
                CommandHandler("set_size", self.set_size),
                CommandHandler("set_amount_of_members", self.set_amount_of_members),
                CommandHandler("remove_chat", self.remove_chat_id)  # manager
            ],
            states={},
            fallbacks=[],
            allow_reentry=True
        )

    def ring_callbacks(self, update: Update, context: CallbackContext):
        callback_function = json.loads(update.callback_query.data)['f']
        if callback_function == 'd':
            self.ring_detail_update(update, context)
            return
        if callback_function == 's':
            self.set_ring_status_callback(update, context)
            return

    def new_ring(self, update: Update, context: CallbackContext):
        chat_id = update.effective_chat.id
        try:
            user = self.unit_of_work.user_repository.get(update.effective_user.id)
        except NoResultFound:
            self.error_view.send_message(chat_id, "Please /register")
            return
        split_text = update.message.text.split(' ', 1)
        if len(split_text) < 2:
            self.error_view.send_message(chat_id, "Please provide a ring name!")
            return
        ring_name = split_text[1]
        ring = Ring(user, ring_name=ring_name)
        self.unit_of_work.ring_repository.add(ring)
        self.ring_view.init_new_ring(chat_id, ring)

    def set_ring_status_command(self, update: Update, context: CallbackContext):
        chat_id = update.effective_chat.id
        ring = self.get_ring_and_handle_exceptions(update)
        if not ring:
            return
        user_id = update.effective_user.id
        if not ring.is_manager(user_id):
            self.error_view.not_manager(chat_id)
            return
        self.ring_view.set_status(chat_id, ring.ring_id)

    def set_ring_status_callback(self, update, context):
        json_data = json.loads(update.callback_query.data)
        ring_id = json_data['r']
        chat_id = update.effective_chat.id
        try:
            ring = self.unit_of_work.ring_repository.get(ring_id)
        except NoResultFound:
            self.error_view.ring_not_found(chat_id)
            return
        if not ring.is_manager(update.effective_user.id):
            self.error_view.send_message(chat_id, "Only the ring manager can set the status!")
            return
        status = RING_STATUS[json_data['s']]
        ring.set_status(status)
        self.unit_of_work.complete()
        update.callback_query.edit_message_text(f"Set ring status to {status.value}", parse_mode=ParseMode.HTML)

    def set_chat_id(self, update: Update, context: CallbackContext):
        try:
            ring_id = int(update.message.text.split(' ', 1)[1])
            ring = self.unit_of_work.ring_repository.get(ring_id)
        except NoResultFound:
            self.error_view.ring_not_found(update.effective_chat.id)
            return
        except InvalidNodeKeyException:
            self.error_view.ring_id_not_provided(update.effective_chat.id)
            return

        if not ring.is_manager(update.effective_user.id):
            self.error_view.not_manager(update.effective_chat.id)
            return
        ring.set_chat_id(update.effective_chat.id)
        self.unit_of_work.complete()
        self.ring_view.message_sender.send_message(update.effective_chat.id, "Chat set!")

    def remove_chat_id(self, update: Update, context: CallbackContext):
        chat_id = update.effective_chat.id
        ring = self.get_ring_and_handle_exceptions(update)
        if not ring:
            return
        if not ring.is_manager(update.effective_user.id):
            self.error_view.not_manager(chat_id)
            return
        ring.remove_chat_id()
        self.unit_of_work.complete()
        self.ring_view.message_sender.send_message(chat_id, "Chat was removed from this ring!")

    def list_rings_of_sender(self, update: Update, context: CallbackContext):
        try:
            rings: [Ring] = self.unit_of_work.ring_repository.get_rings_by_ring_manager(update.effective_user.id)
        except NoResultFound:
            self.error_view.ring_not_found(update.effective_chat.id)
            return
        self.ring_view.list_all_rings_of_ring_manager(update.effective_chat.id, rings)

    def join_ring(self, update: Update, context: CallbackContext):
        chat_id = update.effective_chat.id
        ring: Ring = self.get_ring_and_handle_exceptions(update)
        if not ring:
            return
        try:
            user = self.unit_of_work.user_repository.get(update.effective_user.id)
        except NoResultFound:
            self.error_view.not_registered(chat_id)
            return
        if ring.is_user_member(user):
            self.error_view.send_message(chat_id, "Already in this group")
            return
        ring.add_user(user)
        self.unit_of_work.complete()
        self.ring_view.message_sender.send_message(chat_id, "Welcome to the ring!")

    def leave_ring(self, update: Update, context: CallbackContext):
        chat_id = update.effective_chat.id
        ring = self.get_ring_and_handle_exceptions(update)
        if not ring:
            return
        user_id = update.effective_user.id
        user = self.unit_of_work.user_repository.get(user_id)
        try:
            user = self.unit_of_work.user_repository.get(user_id)
        except NoResultFound:
            self.error_view.send_message(chat_id, "You are not part of this ring!")
            return
        user_in_ring = self.unit_of_work.user_in_ring_repository.find_user_in_ring(ring, user)
        ring.remove_user(user_in_ring)
        self.ring_view.message_sender.send_message("You left the ring!")

    def ring_detail_update(self, update, context: CallbackContext):
        json_data = json.loads(update.callback_query.data)
        ring_id = json_data['r']
        try:
            ring = self.unit_of_work.ring_repository.get(ring_id)
        except NoResultFound:
            self.error_view.ring_not_found(update.effective_chat.id)
            return
        message = detail_ring(ring)
        update.callback_query.edit_message_text(message[0], parse_mode=ParseMode.HTML)

    def get_ring_info(self, update: Update, context: CallbackContext):
        ring = self.get_ring_and_handle_exceptions(update)
        if not ring:
            return
        self.ring_view.send_ring_detail(update.effective_chat.id, ring)

    def get_ring_and_handle_exceptions(self, update: Update):
        chat_id: int = update.effective_chat.id
        try:
            return self.unit_of_work.ring_repository.get_ring(update.message.text, chat_id)
        except NoResultFound:
            self.error_view.ring_not_found(chat_id)
            return
        except InvalidNodeKeyException:
            self.error_view.ring_id_not_provided(chat_id)
            return

    def set_size(self, update: Update, context: CallbackContext):
        split_message = update.message.text.split(' ', 2)
        try:
            ring_id = int(split_message[1])
            print(ring_id)
            ring = self.unit_of_work.ring_repository.get(ring_id)
        except NoResultFound:
            self.error_view.ring_not_found(update.effective_chat.id)
            return
        except InvalidNodeKeyException:
            self.error_view.ring_id_not_provided(update.effective_chat.id)
            return

        if not ring.is_manager(update.effective_user.id):
            self.error_view.not_manager(update.effective_chat.id)
            return
        ring.set_channel_size(int(split_message[2]))
        self.unit_of_work.complete()
        message = f"Ring size set to {ring.channel_size}!"
        if ring.channel_size > 9000:
            message = f"{message} It's over 9000!"
        self.ring_view.message_sender.send_message(update.effective_chat.id, message)

    def set_amount_of_members(self, update: Update, context: CallbackContext):
        split_message = update.message.text.split(' ', 2)
        try:
            ring_id = int(split_message[1])
            print(ring_id)
            ring = self.unit_of_work.ring_repository.get(ring_id)
        except NoResultFound:
            self.error_view.ring_not_found(update.effective_chat.id)
            return
        except InvalidNodeKeyException:
            self.error_view.ring_id_not_provided(update.effective_chat.id)
            return

        if not ring.is_manager(update.effective_user.id):
            self.error_view.not_manager(update.effective_chat.id)
            return
        ring.set_max_ring_members(int(split_message[2]))
        self.unit_of_work.complete()
        message = f"Amount of Ring members is set to {ring.max_ring_members}!"
        if ring.max_ring_members > 26:
            message = f"{message} More than 26 members is discouraged because of a 27 hop limit in LND"
        self.ring_view.message_sender.send_message(update.effective_chat.id, message)
