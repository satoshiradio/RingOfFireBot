from sqlalchemy import Column, Integer, String, ForeignKey, Enum, BigInteger
from sqlalchemy.orm import relationship

from ring_of_fire_bot.model.database import Base

from ring_of_fire_bot.model.ring_status import RING_STATUS
from ring_of_fire_bot.model.user import User
from ring_of_fire_bot.model.user_in_ring import UserInRing


class Ring(Base):
    __tablename__ = 'rings'
    ring_id = Column(Integer, primary_key=True)
    ring_name = Column(String(256), default="")
    status = Column(Enum(RING_STATUS), default=RING_STATUS.WAITING)
    ring_manager_id = Column(Integer, ForeignKey('users.user_id'))
    ring_manager = relationship("User")
    users = relationship("UserInRing", back_populates="ring", cascade="all, delete, delete-orphan")
    max_ring_members = Column(Integer, default=26)
    chat_id = Column(BigInteger, unique=True)
    channel_size = Column(Integer, default=1000000)

    def __init__(self, ring_manager: User, channel_size=1000000, max_ring_members=26, ring_name="",
                 status=RING_STATUS.WAITING):
        self.ring_manager = ring_manager
        self.channel_size = channel_size
        self.max_ring_members = max_ring_members
        self.status = status
        self.ring_name = ring_name

    def set_status(self, status: RING_STATUS):
        self.status = status

    def set_channel_size(self, channel_size: int):
        self.channel_size = channel_size

    def set_max_ring_members(self, max_ring_members: int):
        self.max_ring_members = max_ring_members

    def add_user(self, user: User):
        user_in_ring = UserInRing()

        user_in_ring.user = user
        self.users.append(user_in_ring)

    def remove_user(self, user_in_ring: UserInRing):
        self.users.remove(user_in_ring)

    def is_user_member(self, user: User) -> bool:
        return any(member.user_id == user.user_id for member in self.users)

    def is_manager(self, user_id: int) -> bool:
        return user_id == self.ring_manager.user_id

    def set_chat_id(self, chat_id: int):
        self.chat_id = chat_id

    def remove_chat_id(self):
        self.chat_id = None
