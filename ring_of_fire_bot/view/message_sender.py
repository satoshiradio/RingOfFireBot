import inspect

from telegram import ParseMode, Update, CallbackQuery, ReplyMarkup
from telegram.ext import Updater, CallbackContext, CallbackQueryHandler

from ring_of_fire_bot.utils.utils import get_logger

logger = get_logger()


class MessageSender:
    def __init__(self, updater: Updater):
        self.updater = updater

    def send_message(self, chat_id, text: str, keyboard: ReplyMarkup = None) -> None:
        self.updater.bot.send_message(
            chat_id=chat_id,
            text=f'<b>{text}</b>',
            parse_mode=ParseMode.HTML,
            reply_markup=keyboard,
        )
        logger.info(inspect.stack()[1][3])

    def reply_to_message(self, update: Update, text, keyboard=None):
        update.message.reply_text(text=text, reply_markup=keyboard)

    def update_message(self, query: CallbackQuery, text, keyboard=None):
        query.edit_message_text(text=text, reply_markup=keyboard)

    def button(self, update: Update, context: CallbackContext) -> None:
        query = update.callback_query
        query.answer()
        self.update_message(query, text=f"Selected option: {query.data}", keyboard=query.message.reply_markup)
