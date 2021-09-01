from ring_of_fire_bot.model.user import User
from ring_of_fire_bot.repository.i_user_repository import IUserRepository


class UserRepository(IUserRepository):
    def __init__(self, database):
        self.Model = User
        super().__init__(database)
