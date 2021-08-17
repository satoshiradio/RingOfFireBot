from sqlalchemy import Integer, Column, String
from sqlalchemy.orm import relationship

from ring_of_fire_bot.model.database import Base


class User(Base):
    __tablename__ = 'users'
    user_id = Column(Integer, primary_key=True)
    user_username = Column(String(256))

    def __init__(self, user_id: int, user_username: str):
        self.user_id = user_id
        self.user_username = user_username
