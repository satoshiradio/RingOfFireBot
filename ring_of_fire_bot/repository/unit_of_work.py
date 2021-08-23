import config
from ring_of_fire_bot.model.database import Database
from ring_of_fire_bot.repository.i_ring_repository import IRingRepository
from ring_of_fire_bot.repository.i_unit_of_work import IUnitOfWork
from ring_of_fire_bot.repository.i_user_in_ring_repository import IUserInRingRepository
from ring_of_fire_bot.repository.i_user_repository import IUserRepository
from ring_of_fire_bot.repository.ring_repository import RingRepository
from ring_of_fire_bot.repository.user_in_ring_repository import UserInRingRepository
from ring_of_fire_bot.repository.user_repository import UserRepository


class UnitOfWork(IUnitOfWork):
    def __init__(self):
        self.database = Database(config.DbConfig.SQLALCHEMY_DATABASE_URI)
        self.session = self.database.session()
        # repositories
        self.ring_repository = RingRepository(self.session)
        self.user_repository = UserRepository(self.session)
        self.user_in_ring_repository = UserInRingRepository(self.session)

    @property
    def i_ring_repository(self) -> IRingRepository:
        return self.ring_repository

    @property
    def i_user_repository(self) -> IUserRepository:
        return self.user_repository

    @property
    def i_user_in_ring_repository(self) -> IUserInRingRepository:
        return self.user_in_ring_repository

    def complete(self) -> None:
        self.session.commit()
