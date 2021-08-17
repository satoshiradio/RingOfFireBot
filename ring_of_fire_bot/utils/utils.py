import logging
from abc import abstractmethod

from telegram import Update


def get_logger() -> logging.Logger:
    logger = logging.getLogger()
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
    return logger


@abstractmethod
def is_in_dm(update: Update) -> bool:
    return update.effective_chat.type == "private"
