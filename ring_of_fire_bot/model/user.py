from sqlalchemy import Integer, Column, String
from sqlalchemy.orm import relationship

from ring_of_fire_bot.model.Exceptions.invalid_node_key_exception import InvalidNodeKeyException
from ring_of_fire_bot.model.database import Base

LND_PUBKEY_LENGTH = 66


class User(Base):
    __tablename__ = 'users'
    user_id = Column(Integer, primary_key=True)
    user_username = Column(String(256))
    node_id = Column(String(LND_PUBKEY_LENGTH))
    rings = relationship("UserInRing", back_populates="user", cascade="all, delete, delete-orphan")

    def __init__(self, user_id: int, user_username: str):
        self.user_id = user_id
        self.user_username = user_username

    def set_username(self, username: str):
        self.user_username = username

    def set_node_id(self, node_id: str):
        if len(node_id) != LND_PUBKEY_LENGTH:
            raise InvalidNodeKeyException
        self.node_id = node_id

    def remove_node_id(self):
        self.node_id = None
