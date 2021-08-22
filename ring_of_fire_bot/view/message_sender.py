import inspect

from telegram import ParseMode, Update, CallbackQuery, ReplyMarkup
from telegram.ext import Updater

from ring_of_fire_bot.utils.utils import get_logger

logger = get_logger()


def reply_to_message(update: Update, text, keyboard=None):
    update.message.reply_text(text=text, reply_markup=keyboard)


def update_message(query: CallbackQuery, text, keyboard=None):
    query.edit_message_text(text=text, reply_markup=keyboard)


class MessageSender:
    def __init__(self, updater: Updater):
        self.updater = updater

    def send_message(self, chat_id, text: str, keyboard: ReplyMarkup = None) -> None:
        self.updater.bot.send_message(
            chat_id=chat_id,
            text=text,
            parse_mode=ParseMode.HTML,
            reply_markup=keyboard,
        )
        logger.info(inspect.stack()[1][3])
