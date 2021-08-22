from telegram.ext import Updater

from ring_of_fire_bot.view.message_sender import MessageSender


class UserView:
    welcome_message_text = "Welcome to The Ring Of Fire Bot, to use the bot register your account with /register"
    registered_text = "You successfully registered your account with the Ring Of Fire bot!"
    updated_username_text = "Your username was updated to {}"

    def __init__(self, updater: Updater):
        self.message_sender = MessageSender(updater)

    def welcome_message(self, chat_id: int):
        self.message_sender.send_message(chat_id, self.welcome_message_text)

    def registered(self, chat_id: int):
        self.message_sender.send_message(chat_id, self.registered_text)

    def updated_username(self, chat_id, username):
        self.message_sender.send_message(chat_id, f"Your username was updated to {username}")

    def updated_node_id(self, chat_id: int, node_id: str):
        self.message_sender.send_message(chat_id,
                                         f"""Node id set to <a href="https://amboss.space/node/{node_id}">{node_id}</a>""")
        pass

    def removed_node_id(self, chat_id: int):
        self.message_sender.send_message(chat_id, "The pubkey is removed.")

