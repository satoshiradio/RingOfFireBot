from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup
from telegram.ext import Updater
from telegram.utils.helpers import mention_html

from ring_of_fire_bot.model.ring import Ring
from ring_of_fire_bot.model.ring_status import STATUS
from ring_of_fire_bot.view.message_sender import MessageSender


def detail_ring(ring: Ring):
    chat_id = 0
    text = f"""
ID: {ring.ring_id}
Name: {ring.ring_name}
Status: {ring.status.value}
Channel size: {ring.channel_size}
Max participants: {ring.max_ring_members}
Manager: {mention_html(ring.ring_manager.user_id, ring.ring_manager.user_username)}
Members:"""

    for member in ring.ring_members:
        text = f"""{text}
{mention_html(member.user_id, member.user_username)}"""
    keyboard = InlineKeyboardMarkup
    return chat_id, text, keyboard


class RingView:
    init_text = "New ring was created!"
    rings_of_ring_manager_text = "Select a specific ring:"

    def __init__(self, updater: Updater):
        self.message_sender = MessageSender(updater)

    def init_new_ring(self, chat_id: int):
        self.message_sender.send_message(chat_id, self.init_text)

    def list_all_rings_of_ring_manager(self, chat_id, rings):
        if len(rings) < 1:
            self.message_sender.send_warning(chat_id, "You are not a ring manager of an active ring of fire")
            return
        keyboard = []
        for ring in rings:
            keyboard.append([InlineKeyboardButton(str(ring.ring_id), callback_data=f'ring_detail_{ring.ring_id}')])
        self.message_sender.send_message(chat_id, self.rings_of_ring_manager_text,
                                         keyboard=InlineKeyboardMarkup(keyboard))

    def set_status(self, chat_id, ring_id):
        keyboard = []
        for status in STATUS.list():
            keyboard.append([InlineKeyboardButton(str(status.value),
                                                  callback_data=f'ring_status_{ring_id}_status_{status}')])
        self.message_sender.send_message(chat_id, "Set status of the ring to:", keyboard=InlineKeyboardMarkup(keyboard))
