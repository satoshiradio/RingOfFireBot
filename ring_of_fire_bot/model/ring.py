from sqlalchemy import Column, Integer

from ring_of_fire_bot.model.database import Base


class Ring(Base):
    __tablename__ = 'ring'
    ring_id = Column(Integer, primary_key=True)
    status = Column(Integer, default=0)

    def __init__(self, status=0):
        self.status = status
