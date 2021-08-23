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
                CommandHandler("ring_status", self.set_ring_status_command),  # manager+admins
                CommandHandler("set_chat", self.set_chat_id),  # manager+admins
                CommandHandler("remove_chat", self.remove_chat_id)  # manager+admins
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
        # get user
        try:
            user = self.unit_of_work.i_user_repository.get(update.effective_user.id)
        except NoResultFound:
            self.error_view.message_sender.send_warning(update.effective_chat.id, "Please /register")
            return

        split_text = update.message.text.split(' ', 1)
        if len(split_text) < 2:
            self.error_view.message_sender.send_warning(update.effective_chat.id, "Please provide a ring name!")
            return
        ring_name = split_text[1]
        ring = Ring(user, ring_name=ring_name)
        self.unit_of_work.i_ring_repository.add(ring)
        self.ring_view.init_new_ring(update.effective_chat.id)

    def set_ring_status_command(self, update: Update, context: CallbackContext):
        try:
            ring = self.get_ring(update.message.text, update.effective_chat.id)
        except NoResultFound:
            self.error_view.ring_not_found(update.effective_chat.id)
            return
        except InvalidNodeKeyException:
            self.error_view.ring_id_not_provided(update.effective_chat.id)
            return
        # Only manager can perform this action
        if update.effective_user.id is not ring.ring_manager.id:
            self.error_view.not_manager(update.effective_chat.id)
            return
        if ring.ring_manager_id != update.effective_user.id:
            self.error_view.message_sender.send_warning(update.effective_chat.id, "Only the ring manager can set the "
                                                                                  "Status")
        self.ring_view.set_status(update.effective_chat.id, ring.ring_id)

    def set_ring_status_callback(self, update, context):
        json_data = json.loads(update.callback_query.data)
        ring_id = json_data['r']
        try:
            ring = self.unit_of_work.i_ring_repository.get(ring_id)
        except NoResultFound:
            self.error_view.ring_not_found(update.effective_chat.id)
            return
        # check if ring manager
        if ring.ring_manager_id != update.callback_query.from_user.id:
            self.error_view.message_sender.send_warning("Only the ring manager can set the status!")

        status = RING_STATUS[json_data['s']]
        self.unit_of_work.i_ring_repository.update_ring_status(ring, status)
        update.callback_query.edit_message_text(f"Set ring status to {status.value}", parse_mode=ParseMode.HTML)

    def set_chat_id(self, update: Update, context: CallbackContext):
        try:
            ring_id = int(update.message.text.split(' ', 1)[1])
            ring = self.unit_of_work.i_ring_repository.get(ring_id)
        except NoResultFound:
            self.error_view.ring_not_found(update.effective_chat.id)
            return
        except InvalidNodeKeyException:
            self.error_view.ring_id_not_provided(update.effective_chat.id)
            return
        # Only manager can perform this action
        if update.effective_user.id is not ring.ring_manager.id:
            self.error_view.not_manager(update.effective_chat.id)
            return
        ring.set_chat_id(update.effective_chat.id)
        self.unit_of_work.complete()
        self.ring_view.message_sender.send_message(update.effective_chat.id, "Chat set!")

    def remove_chat_id(self, update: Update, context: CallbackContext):
        try:
            ring = self.get_ring(update.message.text, update.effective_chat.id)
        except NoResultFound:
            self.error_view.ring_not_found(update.effective_chat.id)
            return
        except InvalidNodeKeyException:
            self.error_view.ring_id_not_provided(update.effective_chat.id)
            return
        # Only manager can perform this action
        if update.effective_user.id is not ring.ring_manager.id:
            self.error_view.not_manager(update.effective_chat.id)
            return
        ring.remove_chat_id()
        self.unit_of_work.complete()
        self.ring_view.message_sender.send_message(update.effective_chat.id, "Chat was removed from this ring!")

    def list_rings_of_sender(self, update: Update, context: CallbackContext):
        try:
            rings: [Ring] = self.unit_of_work.i_ring_repository.get_rings_by_ring_manager(update.effective_user.id)
        except NoResultFound:
            self.error_view.ring_not_found(update.effective_chat.id)
            return
        self.ring_view.list_all_rings_of_ring_manager(update.effective_chat.id, rings)

    def join_ring(self, update: Update, context: CallbackContext):
        try:
            ring = self.get_ring(update.message.text, update.effective_chat.id)
        except NoResultFound:
            self.error_view.ring_not_found(update.effective_chat.id)
            return
        except InvalidNodeKeyException:
            self.error_view.ring_id_not_provided(update.effective_chat.id)
            return
        try:
            user = self.unit_of_work.i_ring_repository.get(update.effective_user.id)
        except NoResultFound:
            self.error_view.send_message(update.effective_chat.id, "You are not part of this ring!")
            return
        # check if user is already part of the ring or is the ring manager
        if ring.is_user_member(user):
            self.error_view.message_sender.send_warning(update.effective_chat.id, "Already in this group")
            return
        ring.add_member(user)
        self.unit_of_work.complete()
        self.ring_view.message_sender.send_message(update.effective_chat.id, "Welcome to the ring!")

    def leave_ring(self, update: Update, context: CallbackContext):
        try:
            ring = self.get_ring(update.message.text, update.effective_chat.id)
        except NoResultFound:
            self.error_view.ring_not_found(update.effective_chat.id)
            return
        except InvalidNodeKeyException:
            self.error_view.ring_id_not_provided(update.effective_chat.id)
            return
        user = self.unit_of_work.i_user_repository.get(update.effective_user.id)

        try:
            user = self.unit_of_work.i_user_repository.get(update.effective_user.id)
        except NoResultFound:
            self.error_view.send_message(update.effective_chat.id, "You are not part of this ring!")

        self.unit_of_work.i_ring_repository.remove_user(ring, user)
        self.ring_view.message_sender.send_message("You left the ring!")

    def ring_detail_update(self, update, context: CallbackContext):
        json_data = json.loads(update.callback_query.data)
        ring_id = json_data['r']
        try:
            ring = self.unit_of_work.i_ring_repository.get(ring_id)
        except NoResultFound:
            self.error_view.ring_not_found(update.effective_chat.id)
            return
        message = detail_ring(ring)
        update.callback_query.edit_message_text(message[0], parse_mode=ParseMode.HTML)

    def get_ring_info(self, update: Update, context: CallbackContext):
        try:
            ring = self.get_ring(update.message.text, update.effective_chat.id)
            self.ring_view.send_ring_detail(update.effective_chat.id, ring)
        except NoResultFound:
            self.error_view.ring_not_found(update.effective_chat.id)
            return
        except InvalidNodeKeyException:
            self.error_view.ring_id_not_provided(update.effective_chat.id)
            return

    # can only be used if the only argument is the ring_id
    def get_ring(self, message: str, chat_id: int) -> Ring:
        split_message = message.split(' ')
        # if ring_id is provided find ring with that ID
        if len(split_message) < 2:
            # no ring provided
            ring = self.unit_of_work.i_ring_repository.get_ring_by_chat_id(chat_id)
            if ring:
                return ring
            else:
                raise InvalidNodeKeyException
        # check if chat has a ring
        else:
            ring_id = int(split_message[1])
            return self.unit_of_work.i_ring_repository.get(ring_id)
