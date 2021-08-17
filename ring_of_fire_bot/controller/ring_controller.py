from sqlalchemy.exc import NoResultFound
from telegram import Update, ParseMode
from telegram.ext import CallbackContext, Updater

from ring_of_fire_bot.model.ring import Ring
from ring_of_fire_bot.repository.ring_repository import RingRepository
from ring_of_fire_bot.repository.user_repository import UserRepository
from ring_of_fire_bot.view.error_view import ErrorView
from ring_of_fire_bot.view.ring_view import RingView


class RingController:
    def __init__(self, updater: Updater, ring_repository: RingRepository, user_repository: UserRepository):
        self.updater = updater
        self.ring_repository = ring_repository
        self.user_repository = user_repository
        self.ring_view: RingView = RingView(self.updater)
        self.error_view: ErrorView = ErrorView(self.updater)

    def ring_callbacks(self, update: Update, context: CallbackContext):
        callback_function = update.callback_query.data.split('_', 2)[1]
        print(callback_function)
        if callback_function == 'detail':
            self.ring_detail_update(update, context)
            return

    def new_ring(self, update: Update, context: CallbackContext):
        if update.effective_chat.type != "private":
            self.error_view.not_in_private(update.effective_chat.id)
            return
        # get user
        try:
            user = self.user_repository.get(update.effective_user.id)
            ring = Ring(user)
            self.ring_repository.add(ring)
            self.ring_view.init_new_ring(update.effective_chat.id)
        except NoResultFound:
            self.error_view.message_sender.send_warning(update.effective_chat.id, "Please /register")

    def list_rings_of_sender(self, update: Update, context: CallbackContext):
        rings: [Ring] = self.ring_repository.get_rings_by_ring_manager(update.effective_user.id)
        self.ring_view.list_all_rings_of_ring_manager(update.effective_chat.id, rings)

    def ring_detail_update(self, update, context: CallbackContext):
        ring_id = update.callback_query.data.split('_')[2]
        ring = self.ring_repository.get(ring_id)
        message = self.ring_view.detail_ring(ring)
        print(message[1])
        update.callback_query.edit_message_text(message[1], parse_mode=ParseMode.HTML)
        # self.ring_view.message_sender.send_message(self.ring_view.detail_ring())

    def ring_detail(self, ring_id):
        ring = self.ring_repository.get(ring_id)
        self.ring_view.message_sender.send_message(self.ring_view.detail_ring(ring))
