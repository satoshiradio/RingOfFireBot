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
    chat_id = Column(Integer, unique=True)
    channel_size = Column(Integer, default=1000000)

    def __init__(self, ring_manager: User, channel_size=1000000, max_ring_members=26, ring_name="",
                 status=STATUS.WAITING_ON_PARTICIPANTS):
        self.ring_manager = ring_manager
        self.channel_size = channel_size
        self.max_ring_members = max_ring_members
        self.status = status
        self.ring_members.append(ring_manager)
        self.ring_name = ring_name

    def set_status(self, status: STATUS):
        self.status = status

    def set_channel_size(self, channel_size: int):
        self.channel_size = channel_size

    def set_max_ring_members(self, max_ring_members: int):
        self.max_ring_members = max_ring_members

    def add_member(self, member: User):
        self.ring_members.append(member)

    def is_user_member(self, user: User) -> bool:
        return any(member.user_id == user.user_id for member in self.ring_members)

    def is_manager(self, user: User) -> bool:
        return user.user_id == self.ring_manager_id

    def set_chat_id(self, chat_id: int):
        self.chat_id = chat_id

    def remove_chat_id(self):
        self.chat_id = None
