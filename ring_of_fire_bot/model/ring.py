from sqlalchemy import Column, Integer, String, ForeignKey, Enum, Table
from sqlalchemy.orm import relationship

from ring_of_fire_bot.model.database import Base
from ring_of_fire_bot.model.ring_status import STATUS
from ring_of_fire_bot.model.user import User

association_table = Table('ringUserTable', Base.metadata,
                          Column('ring_id', ForeignKey('rings.ring_id'), primary_key=True),
                          Column('user_id', ForeignKey('users.user_id'), primary_key=True)
                          )


class Ring(Base):
    __tablename__ = 'rings'
    ring_id = Column(Integer, primary_key=True)
    ring_name = Column(String(256), default="")
    status = Column(Enum(STATUS), default=STATUS.WAITING_ON_PARTICIPANTS)
    ring_manager_id = Column(Integer, ForeignKey('users.user_id'))
    ring_manager = relationship("User")
    ring_members = relationship("User", secondary=association_table)
    max_ring_members = Column(Integer, default=26)
    channel_size = Column(Integer, default=1000000)

    def __init__(self, ring_manager: User, channel_size=1000000, max_ring_members=26, ring_name="",
                 status=STATUS.WAITING_ON_PARTICIPANTS):
        self.ring_manager = ring_manager
        self.channel_size = channel_size
        self.max_ring_members = max_ring_members
        self.status = status
        self.ring_members.append(ring_manager)
        self.ring_name = ring_name
