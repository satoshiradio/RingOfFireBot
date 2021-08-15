import config
from ring_of_fire_bot.model.database import Database
from ring_of_fire_bot.model.ring import Ring
from ring_of_fire_bot.repository.ring_repository import RingRepository


class RingOfFire:
    def __init__(self):
        self.database = Database(config.DbConfig.SQLALCHEMY_DATABASE_URI)
        self.ring_repository = RingRepository(self.database)



def main():
    RingOfFire()
    pass


if __name__ == "__main__":
    main()
