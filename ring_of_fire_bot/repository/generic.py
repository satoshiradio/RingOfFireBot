from typing import Generic, TypeVar, Type

from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Session

from ring_of_fire_bot.model.database import Base

ModelType = TypeVar("ModelType", bound=Base)


class Repository(Generic[ModelType]):
    Model: Type[ModelType] = None

    def __init__(self, session):
        if self.Model is None:
            raise Exception(
                self, "model", "This should be set to a Model class.",
            )
        self._session: Session = session
        self.query = self._new_query()
        self.offset = None
        self.size = None

    def _new_query(self):
        return self._session.query(self.Model)

    def build(self):
        query = self.query
        if self.size:
            query = query.limit(self.size)
        if self.offset:
            query = query.offset(self.offset)
        self.query = self._new_query()
        return query

    def get(self, entity_id, should_error=True) -> ModelType:
        result = self._new_query().get(entity_id)
        if not result and should_error:
            raise NoResultFound("No result was found.")
        return result

    def all(self) -> [ModelType]:
        return self.build().all()

    def add(self, item: ModelType):
        self._session.add(item)
        self._session.commit()
        return item
