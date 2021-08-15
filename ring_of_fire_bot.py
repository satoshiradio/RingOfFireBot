from telegram.ext import Updater

import config
from ring_of_fire_bot.controller.bot_controller import BotController
from ring_of_fire_bot.model.database import Database
from ring_of_fire_bot.model.ring import Ring
from ring_of_fire_bot.repository.ring_repository import RingRepository


class RingOfFire:
    def __init__(self, dispatcher):
        self.database = Database(config.DbConfig.SQLALCHEMY_DATABASE_URI)
        self.ring_repository = RingRepository(self.database)
        self.botController = BotController(dispatcher=dispatcher)


def main():
    updater = Updater(token=config.BotConfig.TOKEN, use_context=True)
    dispatcher = updater.dispatcher
    RingOfFire(dispatcher)
    updater.start_polling(poll_interval=1)
    updater.idle()


if __name__ == "__main__":
    main()
