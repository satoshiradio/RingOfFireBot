import json

from telegram import Update
from telegram.ext import ConversationHandler, CommandHandler, CallbackContext, CallbackQueryHandler, Updater

from ring_of_fire_bot.controller.error_controller import error_handler
from ring_of_fire_bot.controller.ring_controller import RingController
from ring_of_fire_bot.controller.user_controller import UserController
from ring_of_fire_bot.controller.user_in_ring_controller import UserInRingController
from ring_of_fire_bot.repository.i_unit_of_work import IUnitOfWork
from ring_of_fire_bot.view.error_view import ErrorView
from ring_of_fire_bot.view.welcome_view import WelcomeView


class BotController:
    def __init__(self, updater: Updater, unit_of_work: IUnitOfWork) -> None:
        # Telegram
        self.updater = updater
        self.dispatcher = self.updater.dispatcher
        # Unit of Work
        self.unit_of_work = unit_of_work
        # controllers
        self.ring_controller = RingController(self.updater, self.unit_of_work)
        self.user_controller = UserController(self.updater, self.unit_of_work)
        self.user_in_ring_controller = UserInRingController(self.updater, self.unit_of_work)
        # Views
        self.welcome_view: WelcomeView = WelcomeView(self.updater)
        self.error_view: ErrorView = ErrorView(self.updater)
        # handlers
        self.__process_handlers()
        self.dispatcher.add_handler(CallbackQueryHandler(self.__process_callbacks))

    def welcome_message(self, update: Update, context: CallbackContext):
        self.welcome_view.send_welcome_message(update.effective_chat.id)

    def __process_callbacks(self, update: Update, context: CallbackContext) -> None:
        query = update.callback_query
        query.answer()
        if json.loads(update.callback_query.data)['c'] == 'r':
            self.ring_controller.ring_callbacks(update, context)

        if json.loads(update.callback_query.data)['c'] == 'uir':
            self.user_in_ring_controller.callbacks(update, context)

    def __process_handlers(self):
        conversation_handler = ConversationHandler(entry_points=[
            CommandHandler("start", self.welcome_message)
        ],
            states={}, fallbacks=[], allow_reentry=True)
        self.dispatcher.add_handler(self.ring_controller.get_commands())
        self.dispatcher.add_handler(self.user_controller.get_commands())
        self.dispatcher.add_handler(self.user_in_ring_controller.get_commands())
        self.dispatcher.add_handler(conversation_handler)
        self.dispatcher.add_error_handler(error_handler)
