from telegram.ext import Updater

import config
from ring_of_fire_bot.controller.bot_controller import BotController
from ring_of_fire_bot.repository.i_unit_of_work import IUnitOfWork
from ring_of_fire_bot.repository.unit_of_work import UnitOfWork
from ring_of_fire_bot.view.message_sender import MessageSender

POLL_INTERVAL = 1


class RingOfFire:
    def __init__(self, updater: Updater):
        # TG Bot
        self.updater = updater
        self.message_sender = MessageSender(self.updater)
        self.dispatcher = self.updater.dispatcher

        # Unit of Work
        self.unit_of_work: IUnitOfWork = UnitOfWork()

        # Controllers
        self.bot_controller = BotController(self.updater, self.unit_of_work)


def main():
    updater = Updater(token=config.BotConfig.TOKEN, use_context=True)
    RingOfFire(updater)
    updater.start_polling(poll_interval=POLL_INTERVAL)
    updater.idle()


if __name__ == "__main__":
    main()
