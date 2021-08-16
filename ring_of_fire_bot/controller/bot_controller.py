from telegram import Update
from telegram.ext import ConversationHandler, CommandHandler, CallbackContext, CallbackQueryHandler, Updater

from ring_of_fire_bot.controller.ring_controller import RingController
from ring_of_fire_bot.model.ring import Ring
from ring_of_fire_bot.repository.ring_repository import RingRepository
from ring_of_fire_bot.view.error_view import ErrorView
from ring_of_fire_bot.view.ring_view import RingView
from ring_of_fire_bot.view.welcome_view import WelcomeView


class BotController:
    def __init__(self, updater: Updater, ring_repository: RingRepository) -> None:
        self.updater = updater
        self.dispatcher = self.updater.dispatcher

        self.dispatcher.add_handler(CallbackQueryHandler(self.__process_callbacks))
        # repositories
        self.ring_repository = ring_repository
        # controllers
        self.ring_controller = RingController(self.updater, self.ring_repository)
        # Views
        self.welcome_view: WelcomeView = WelcomeView(self.updater)
        self.error_view: ErrorView = ErrorView(self.updater)

        # handlers
        self.__process_handlers()

    def welcome_message(self, update: Update, context: CallbackContext):
        self.welcome_view.send_welcome_message(update.effective_chat.id)

    def __process_callbacks(self, update: Update, context: CallbackContext) -> None:
        query = update.callback_query
        query.answer()

    def __process_handlers(self):
        conversation_handler = ConversationHandler(entry_points=[
            CommandHandler("start", self.welcome_message),
            CommandHandler("new_ring", self.ring_controller.new_ring),
            CommandHandler("my_rings", self.ring_controller.list_rings_of_sender)
        ],
            states={}, fallbacks=[], allow_reentry=True)
        self.dispatcher.add_handler(conversation_handler)
