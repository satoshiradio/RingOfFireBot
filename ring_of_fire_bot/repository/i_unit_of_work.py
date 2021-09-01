from abc import ABC, abstractmethod

from ring_of_fire_bot.repository.i_ring_repository import IRingRepository
from ring_of_fire_bot.repository.i_user_in_ring_repository import IUserInRingRepository
from ring_of_fire_bot.repository.i_user_repository import IUserRepository


class IUnitOfWork(ABC):
    @property
    @abstractmethod
    def ring_repository(self) -> IRingRepository:
        raise NotImplementedError

    @property
    @abstractmethod
    def user_repository(self) -> IUserRepository:
        raise NotImplementedError

    @property
    @abstractmethod
    def user_in_ring_repository(self) -> IUserInRingRepository:
        raise NotImplementedError

    @abstractmethod
    def complete(self) -> int:
        raise NotImplementedError
