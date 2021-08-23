from abc import ABC, abstractmethod
from typing import Generic, TypeVar

from ring_of_fire_bot.model.database import Base

ModelType = TypeVar("ModelType", bound=Base)


class IRepository(ABC, Generic[ModelType]):
    @abstractmethod
    def get(self, entity_id, should_error=True) -> ModelType:
        raise NotImplementedError

    @abstractmethod
    def all(self) -> [ModelType]:
        raise NotImplementedError

    @abstractmethod
    def add(self, item: ModelType) -> ModelType:
        raise NotImplementedError

    @abstractmethod
    def remove(self, item: ModelType):
        raise NotImplementedError

    @abstractmethod
    def remove_range(self, items: [ModelType]):
        raise NotImplementedError
