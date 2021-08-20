from ring_of_fire_bot.model.user import User
from ring_of_fire_bot.repository.generic import Repository


class UserRepository(Repository[User]):
    def __init__(self, database):
        self.Model = User
        super().__init__(database)

    def update_username(self, entity_id, username: str):
        user = self.get(entity_id)
        user.set_username(username)
        self._session.commit()
