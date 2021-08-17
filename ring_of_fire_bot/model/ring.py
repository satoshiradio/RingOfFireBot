from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from ring_of_fire_bot.model.database import Base


class Ring(Base):
    __tablename__ = 'rings'
    ring_id = Column(Integer, primary_key=True)
    status = Column(Integer, default=0)
    ring_manager_id = Column(Integer, ForeignKey('users.user_id'))
    ring_manager = relationship("User")

    def __init__(self, ring_manager, status=0):
        self.ring_manager = ring_manager
        self.status = status
