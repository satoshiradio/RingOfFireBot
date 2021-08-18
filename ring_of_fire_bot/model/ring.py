from sqlalchemy import Column, Integer

from ring_of_fire_bot.model.database import Base
from ring_of_fire_bot.model.ring_status import STATUS


class Ring(Base):
    __tablename__ = 'ring'
    ring_id = Column(Integer, primary_key=True)
    status = Column(Integer, default=0)

    def __init__(self, status=STATUS.WAITING_ON_PARTICIPANTS):
        self.status = status
