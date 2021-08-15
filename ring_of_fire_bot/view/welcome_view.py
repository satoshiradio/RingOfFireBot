from ring_of_fire_bot.view.message_sender import MessageSender


class WelcomeView:
    welcome_message = "Welcome to the Ring Of Fire Bot!"

    def __init__(self, message_sender: MessageSender):
        self.message_sender = message_sender

    def send_welcome_message(self, chat_id) -> None:
        self.message_sender.send_message(chat_id, self.welcome_message)
