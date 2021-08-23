from telegram import ReplyMarkup
from telegram.ext import Updater

from ring_of_fire_bot.view.message_sender import MessageSender


class ErrorView:
    not_in_private_text = "This message must be sent in a DM"

    def __init__(self, updater: Updater):
        self.message_sender = MessageSender(updater)

    def send_message(self, chat_id, text: str, keyboard: ReplyMarkup = None) -> None:
        formatted_text = f'⚠<b>{text}</b>⚠'
        self.message_sender.send_message(chat_id, formatted_text, keyboard)

    def not_in_private(self, chat_id: int):
        self.send_message(chat_id, text=self.not_in_private_text)

    def ring_not_found(self, chat_id: int):
        self.send_message(chat_id, "No ring found with provided ring id, please provide a valid ring id.")

    def ring_id_not_provided(self, chat_id: int):
        self.send_message(chat_id, "Please provide a valid ring id or register this chat with /set_chat {node id}")

    def not_manager(self, chat_id: id):
        self.send_message(chat_id, "Only the ring manager can perform this action")

    def not_registered(self, chat_id: id):
        self.send_message(chat_id, "The bot doesn't know you, please /register")
