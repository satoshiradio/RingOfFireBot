

from sqlalchemy import Column, ForeignKey, Boolean, Enum
from sqlalchemy.orm import relationship

from ring_of_fire_bot.model.channel_status import CHANNEL_STATUS
from ring_of_fire_bot.model.database import Base


class UserInRing(Base):
    __tablename__ = 'user_in_ring'
    ring_id = Column(ForeignKey('rings.ring_id'), primary_key=True)
    user_id = Column(ForeignKey('users.user_id'), primary_key=True)
    is_funded = Column(Boolean, default=False)
    channel_status = Column(Enum(CHANNEL_STATUS), default=CHANNEL_STATUS.NOT_OPEN)
    ring = relationship("Ring", back_populates="users")
    user = relationship("User", back_populates="rings")
