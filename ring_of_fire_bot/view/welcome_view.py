from telegram.ext import Updater

from ring_of_fire_bot.view.message_sender import MessageSender


class WelcomeView:
    welcome_message = "Welcome to the Ring Of Fire Bot!"

    def __init__(self, updater: Updater):
        self.message_sender = MessageSender(updater)

    def send_welcome_message(self, chat_id) -> None:
        self.message_sender.send_message(chat_id, self.welcome_message)
