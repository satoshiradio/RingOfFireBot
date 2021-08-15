from telegram import Update
from telegram.ext import ConversationHandler, CommandHandler, CallbackContext


class BotController:
    def __init__(self, dispatcher):
        self.dispatcher = dispatcher
        self.__process_handlers()

    @staticmethod
    def welcome_message(update: Update, context: CallbackContext):
        update.message.reply_text(
            "Welcome to the Ring Of Fire Bot!"
        )

    def __process_handlers(self):
        conversation_handler = ConversationHandler(entry_points=[CommandHandler("start", self.welcome_message)],
                                                   states={}, fallbacks=[], allow_reentry=True)
        self.dispatcher.add_handler(conversation_handler)
