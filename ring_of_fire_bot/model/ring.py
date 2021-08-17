from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from ring_of_fire_bot.model.database import Base
from ring_of_fire_bot.model.ring_status import STATUS


class Ring(Base):
    __tablename__ = 'rings'
    ring_id = Column(Integer, primary_key=True)
    status = Column(Integer, default=0)
    ring_manager_id = Column(Integer, ForeignKey('users.user_id'))
    ring_manager = relationship("User")

    def __init__(self, ring_manager, status=STATUS.WAITING_ON_PARTICIPANTS):
        self.ring_manager = ring_manager
        self.status = status
