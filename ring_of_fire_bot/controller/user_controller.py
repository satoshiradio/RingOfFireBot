from sqlalchemy.exc import NoResultFound
from telegram import Update
from telegram.ext import Updater, CallbackContext, ConversationHandler, CommandHandler

from ring_of_fire_bot.model.Exceptions.invalid_node_key_exception import InvalidNodeKeyException
from ring_of_fire_bot.model.user import User
from ring_of_fire_bot.repository.i_unit_of_work import IUnitOfWork
from ring_of_fire_bot.utils.utils import is_in_dm
from ring_of_fire_bot.view.error_view import ErrorView
from ring_of_fire_bot.view.user_view import UserView


class UserController:
    def __init__(self, updater: Updater, unit_of_work: IUnitOfWork):
        self.updater = updater
        self.unit_of_work = unit_of_work
        self.userView: UserView = UserView(self.updater)
        self.error_view: ErrorView = ErrorView(self.updater)

    def get_commands(self):
        return ConversationHandler(entry_points=[
            CommandHandler("register", self.register),
            CommandHandler("update_username", self.update_username),
            CommandHandler("set_node_id", self.set_node_id),
            CommandHandler("remove_node_id", self.remove_node_id)
        ],
            states={}, fallbacks=[], allow_reentry=True)

    def register(self, update: Update, context: CallbackContext):
        # check if in DM
        if not is_in_dm(update):
            self.error_view.not_in_private(update.effective_chat.id)
            return

        sender = update.effective_user
        try:
            _ = self.unit_of_work.user_repository.get(sender.id)
            # if user_repository.get does not throw a NoResultFound exception the user has already registered
            self.error_view.send_message(update.effective_chat.id, "You are already registered!")
        except NoResultFound:
            user = User(sender.id, sender.username)
            self.unit_of_work.user_repository.add(user)
            self.userView.registered(update.effective_chat.id)
            return

    def update_username(self, update: Update, context: CallbackContext):
        if not is_in_dm(update):
            self.error_view.not_in_private(update.effective_chat.id)
            return
        try:
            user = self.unit_of_work.user_repository.get(update.effective_user.id)
            user.set_username(update.effective_user.username)
            self.unit_of_work.complete()
            self.userView.updated_username(update.effective_chat.id, user.user_username)
        except NoResultFound:
            self.error_view.send_message(update.effective_chat.id, "Please /register before updating "
                                                                   "your username")

    def set_node_id(self, update: Update, context: CallbackContext):
        node_id = update.message.text.split(' ', 1)[1]
        if not is_in_dm(update):
            self.error_view.not_in_private(update.effective_chat.id)
            return
        try:
            user = self.unit_of_work.user_repository.get(update.effective_user.id)
            user.set_node_id(node_id)
            self.unit_of_work.complete()
            self.userView.updated_node_id(update.effective_chat.id, node_id)
        except NoResultFound:
            self.error_view.send_message(update.effective_chat.id, "Please /register before updating "
                                                                   "your node id")
        except InvalidNodeKeyException:
            self.error_view.send_message(update.effective_chat.id, "The node id is invalid")

    def remove_node_id(self, update: Update, context: CallbackContext):
        if not is_in_dm(update):
            self.error_view.not_in_private(update.effective_chat.id)
            return
        try:
            user: User = self.unit_of_work.user_repository.get(update.effective_user.id)
            user.remove_node_id()
            self.unit_of_work.complete()
            self.userView.removed_node_id(update.effective_chat.id)
        except NoResultFound:
            self.error_view.send_message(update.effective_chat.id, "Please /register before removing your node id")
        except InvalidNodeKeyException:
            self.error_view.send_message(update.effective_chat.id, "The node id is invalid")
