from telegram.ext import Updater

import config
from ring_of_fire_bot.controller.bot_controller import BotController
from ring_of_fire_bot.model.database import Database
from ring_of_fire_bot.model.ring import Ring
from ring_of_fire_bot.repository.ring_repository import RingRepository
from ring_of_fire_bot.view.message_sender import MessageSender

POLL_INTERVAL = 1


class RingOfFire:
    def __init__(self, updater: Updater):
        self.database = Database(config.DbConfig.SQLALCHEMY_DATABASE_URI)
        self.ring_repository = RingRepository(self.database)
        self.updater = updater
        self.message_sender = MessageSender(self.updater)
        self.dispatcher = self.updater.dispatcher
        self.bot_controller = BotController(updater=self.updater, message_sender=self.message_sender)


def main():
    updater = Updater(token=config.BotConfig.TOKEN, use_context=True)
    RingOfFire(updater)
    updater.start_polling(poll_interval=POLL_INTERVAL)
    updater.idle()


if __name__ == "__main__":
    main()
