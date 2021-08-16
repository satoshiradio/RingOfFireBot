from telegram import Update
from telegram.ext import CallbackContext, Updater

from ring_of_fire_bot.model.ring import Ring
from ring_of_fire_bot.repository.ring_repository import RingRepository
from ring_of_fire_bot.view.error_view import ErrorView
from ring_of_fire_bot.view.ring_view import RingView


class RingController:
    def __init__(self, updater: Updater, ring_repository: RingRepository):
        self.updater = updater
        self.ring_repository = ring_repository
        self.ring_view: RingView = RingView(self.updater)
        self.error_view: ErrorView = ErrorView(self.updater)

    def new_ring(self, update: Update, context: CallbackContext):
        if update.effective_chat.type != "private":
            self.error_view.not_in_private(update.effective_chat.id)
            return
        ring = Ring(ring_manager=update.effective_user.id)
        self.ring_repository.add(ring)
        self.ring_view.init_new_ring(update.effective_chat.id)

    def list_rings_of_sender(self, update: Update, context: CallbackContext):
        rings: [Ring] = self.ring_repository.get_rings_by_ring_manager(update.effective_user.id)
        self.ring_view.list_all_rings_of_ring_manager(update.effective_chat.id, rings)
