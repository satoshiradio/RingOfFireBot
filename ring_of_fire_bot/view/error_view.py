from telegram.ext import Updater

from ring_of_fire_bot.view.message_sender import MessageSender


class ErrorView:
    not_in_private_text = "This message must be sent in a DM"

    def __init__(self, updater: Updater):
        self.message_sender = MessageSender(updater)

    def not_in_private(self, chat_id: int):
        self.message_sender.send_warning(chat_id, text=self.not_in_private_text)
