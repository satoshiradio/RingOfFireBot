from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup
from telegram.ext import Updater

from ring_of_fire_bot.view.message_sender import MessageSender


class RingView:
    init_text = "Test"
    rings_of_ring_manager_text = "Select a specific ring:"

    def __init__(self, updater: Updater):
        self.message_sender = MessageSender(updater)

    def init_new_ring(self, chat_id: int):
        self.message_sender.send_message(chat_id, self.init_text)

    def list_all_rings_of_ring_manager(self, chat_id, rings):
        keyboard = []
        for ring in rings:
            keyboard.append([InlineKeyboardButton(str(ring.ring_id), callback_data=f'ring_detail-{ring.ring_id}')])
        self.message_sender.send_message(chat_id, self.rings_of_ring_manager_text,
                                         keyboard=InlineKeyboardMarkup(keyboard))
