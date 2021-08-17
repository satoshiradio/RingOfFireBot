from sqlalchemy.exc import NoResultFound
from telegram import Update
from telegram.ext import Updater, CallbackContext

from ring_of_fire_bot.model.user import User
from ring_of_fire_bot.repository.user_repository import UserRepository
from ring_of_fire_bot.utils.utils import is_in_dm
from ring_of_fire_bot.view.error_view import ErrorView
from ring_of_fire_bot.view.user_view import UserView


class UserController:
    def __init__(self, updater: Updater, user_repository: UserRepository):
        self.updater = updater
        self.user_repository = user_repository
        self.userView: UserView = UserView(self.updater)
        self.error_view: ErrorView = ErrorView(self.updater)

    def register(self, update: Update, context: CallbackContext):
        # check if in DM
        if not is_in_dm(update):
            self.error_view.not_in_private(update.effective_chat.id)
            return

        sender = update.effective_user
        try:
            _ = self.user_repository.get(sender.id)
            # if user_repository.get does not throw a NoResultFound exception the user has already registered
            self.error_view.message_sender.send_warning(update.effective_chat.id, "You are already registered!")
        except NoResultFound:
            user = User(sender.id, sender.username)
            self.user_repository.add(user)
            self.userView.registered(update.effective_chat.id)
            return

    def update_username(self, update: Update, context: CallbackContext):
        if not is_in_dm(update):
            self.error_view.not_in_private(update.effective_chat.id)
            return
        try:
            user = self.user_repository.get(update.effective_user.id)
            self.user_repository.update_username(user.user_id, user.user_username)
            self.userView.updated_username(update.effective_chat.id, update.effective_user.username)
        except NoResultFound:
            self.error_view.message_sender.send_warning(update.effective_chat.id, "Please /register before updating "
                                                                                  "your username")
