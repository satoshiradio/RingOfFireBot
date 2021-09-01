import json

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyMarkup
from telegram.ext import Updater
from telegram.utils.helpers import mention_html

from ring_of_fire_bot.model.channel_status import CHANNEL_STATUS
from ring_of_fire_bot.model.ring import Ring
from ring_of_fire_bot.model.ring_status import RING_STATUS
from ring_of_fire_bot.view.message_sender import MessageSender


def detail_ring(ring: Ring):
    text = f"""
ID: {ring.ring_id}
Name: {ring.ring_name}
Status: {ring.status.value}
Channel size: {ring.channel_size}
Max participants: {ring.max_ring_members}
Manager: {mention_html(ring.ring_manager.user_id, ring.ring_manager.user_username)}
Members:"""

    for userInRing in ring.users:
        text = f"""{text}
{mention_html(userInRing.user.user_id, userInRing.user.user_username)}"""
        if userInRing.is_funded:
            text = f"{text}🙌🏻"
        if userInRing.channel_status == CHANNEL_STATUS.PENDING:
            text = f"{text}⏳"
        if userInRing.channel_status == CHANNEL_STATUS.OPEN:
            text = f"{text}✅"
        if userInRing.user.node_id:
            text = f"""{text}
{userInRing.user.node_id}

"""
        else:
            text = f"""{text}
Node id not set

"""

    keyboard = InlineKeyboardMarkup
    return text, keyboard


class RingView:
    init_text = "New ring was created!"
    rings_of_ring_manager_text = "Select a specific ring:"

    def __init__(self, updater: Updater):
        self.message_sender = MessageSender(updater)

    def send_message(self, chat_id, text: str, keyboard: ReplyMarkup = None) -> None:
        self.message_sender.send_message(chat_id, text, keyboard)

    def init_new_ring(self, chat_id: int, ring: Ring):
        self.message_sender.send_message(chat_id, f"{self.init_text} Ring id is {ring.ring_id}")

    def send_ring_detail(self, chat_id: int, ring: Ring):
        detail = detail_ring(ring)
        self.send_message(chat_id, detail[0])

    def list_all_rings_of_ring_manager(self, chat_id, rings):
        if len(rings) < 1:
            self.message_sender.send_message(chat_id, "You are not a ring manager of an active ring of fire")
            return
        keyboard = []

        for ring in rings:
            json_data = {'c': 'r',
                         'f': 'd',
                         'r': ring.ring_id
                         }
            keyboard.append([InlineKeyboardButton(str(ring.ring_id), callback_data=json.dumps(json_data))])
        self.message_sender.send_message(chat_id, self.rings_of_ring_manager_text,
                                         keyboard=InlineKeyboardMarkup(keyboard))

    def set_status(self, chat_id, ring_id):
        keyboard = []
        for status in RING_STATUS.list():
            # c = controller, f = function, r = ring_id, s = status
            # using chars because otherwise the data is to big, only 64 utf-8 bytes allowed
            json_data = {'c': 'r',
                         'f': 's',
                         'r': ring_id,
                         's': str(status.name)
                         }

            keyboard.append([InlineKeyboardButton(str(status.value),
                                                  callback_data=json.dumps(json_data))])
        self.message_sender.send_message(chat_id, "Set status of the ring to:", keyboard=InlineKeyboardMarkup(keyboard))

    def set_channel_status(self, chat_id, ring_id, user_id):
        keyboard = []

        for status in CHANNEL_STATUS.list():
            json_data = {'c': 'uir',
                         'f': 'c',
                         'r': ring_id,
                         'u': user_id,
                         's': str(status.name)
                         }
            print(json_data)
            keyboard.append([InlineKeyboardButton(str(status.value),
                                                  callback_data=json.dumps(json_data))])
        self.message_sender.send_message(chat_id, "Set channel status to:",
                                         keyboard=InlineKeyboardMarkup(keyboard))

    def set_funded(self, chat_id, ring_id, user_id):

        keyboard = []

        false = {'c': 'uir',
                 'f': 'f',
                 'r': ring_id,
                 'u': user_id,
                 's': False
                 }
        ready = {'c': 'uir',
                 'f': 'f',
                 'r': ring_id,
                 'u': user_id,
                 's': True
                 }
        keyboard.append(
            [InlineKeyboardButton("Not yet",
                                  callback_data=json.dumps(false))],
        )
        keyboard.append(
            [InlineKeyboardButton("Sats are ready",
                                  callback_data=json.dumps(ready))],
        )
        self.message_sender.send_message(chat_id, "Set channel status to:",
                                         keyboard=InlineKeyboardMarkup(keyboard))
