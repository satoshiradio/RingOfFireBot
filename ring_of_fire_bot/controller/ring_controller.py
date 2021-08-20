import json

from sqlalchemy.exc import NoResultFound
from telegram import Update, ParseMode
from telegram.ext import CallbackContext, Updater

from ring_of_fire_bot.model.ring import Ring
from ring_of_fire_bot.model.ring_status import STATUS
from ring_of_fire_bot.repository.ring_repository import RingRepository
from ring_of_fire_bot.repository.user_repository import UserRepository
from ring_of_fire_bot.view.error_view import ErrorView
from ring_of_fire_bot.view.ring_view import RingView, detail_ring


def is_member_of_ring(ring: Ring, user_id: int) -> bool:
    return any(member.user_id == user_id for member in ring.ring_members)


class RingController:
    def __init__(self, updater: Updater, ring_repository: RingRepository, user_repository: UserRepository):
        self.updater = updater
        self.ring_repository = ring_repository
        self.user_repository = user_repository
        self.ring_view: RingView = RingView(self.updater)
        self.error_view: ErrorView = ErrorView(self.updater)

    def ring_callbacks(self, update: Update, context: CallbackContext):
        callback_function = json.loads(update.callback_query.data)['function']
        if callback_function == 'detail':
            self.ring_detail_update(update, context)
            return
        if callback_function == 'status':
            self.set_ring_status_callback(update, context)
            return

    def new_ring(self, update: Update, context: CallbackContext):
        if update.effective_chat.type != "private":
            self.error_view.not_in_private(update.effective_chat.id)
            return
        # get user
        try:
            user = self.user_repository.get(update.effective_user.id)
            ring_name = update.message.text.split(' ', 1)[1]
            ring = Ring(user, ring_name=ring_name)
            self.ring_repository.add(ring)
            self.ring_view.init_new_ring(update.effective_chat.id)
        except NoResultFound:
            self.error_view.message_sender.send_warning(update.effective_chat.id, "Please /register")

    def set_ring_status_command(self, update: Update, context: CallbackContext):
        ring_id = update.message.text.split(' ', 1)[1]
        self.ring_view.set_status(update.effective_chat.id, ring_id)

    def set_ring_status_callback(self, update, context):
        json_data = json.loads(update.callback_query.data)
        ring_id = json_data['ring_id']
        ring = self.ring_repository.get(ring_id)
        # check if ring manager
        if ring.ring_manager_id != update.callback_query.from_user.id:
            self.error_view.message_sender.send_warning("Only the ring manager can set the status!")

        status = STATUS[json_data['status']]
        self.ring_repository.update_ring_status(ring_id, status)
        update.callback_query.edit_message_text(f"Set ring status to {status.value}", parse_mode=ParseMode.HTML)

    def list_rings_of_sender(self, update: Update, context: CallbackContext):
        rings: [Ring] = self.ring_repository.get_rings_by_ring_manager(update.effective_user.id)
        self.ring_view.list_all_rings_of_ring_manager(update.effective_chat.id, rings)

    def join_ring(self, update: Update, context: CallbackContext):
        ring_id = update.message.text.split(' ', 1)[1]
        ring = self.ring_repository.get(ring_id)
        user = self.user_repository.get(update.effective_user.id)
        # check if user is already part of the ring or is the ring manager
        if is_member_of_ring(ring, update.effective_user.id) or ring.ring_manager_id == update.effective_user.id:
            self.error_view.message_sender.send_warning(update.effective_chat.id, "Already in this group")
            return
        self.ring_repository.add_member_to_ring(ring_id, user)

    def ring_detail_update(self, update, context: CallbackContext):
        json_data = json.loads(update.callback_query.data)
        ring_id = json_data['ring_id']
        ring = self.ring_repository.get(ring_id)
        message = detail_ring(ring)
        print(message[1])
        update.callback_query.edit_message_text(message[1], parse_mode=ParseMode.HTML)
        # self.ring_view.message_sender.send_message(self.ring_view.detail_ring())

    def ring_detail(self, ring_id):
        ring = self.ring_repository.get(ring_id)
        self.ring_view.message_sender.send_message(detail_ring(ring))

    def get_ring_info(self, update: Update, context: CallbackContext):
        split_message = update.message.text.split(' ')
        if len(split_message) < 2:
            self.error_view.message_sender.send_warning(update.effective_chat.id, "Provide an ring ID")
            return
        ring_id = split_message[1]
        ring = self.ring_repository.get(ring_id)
        self.ring_view.message_sender.send_message(update.effective_chat.id, detail_ring(ring)[1])
