from ring_of_fire_bot.model.user import User
from ring_of_fire_bot.repository.generic import Repository


class UserRepository(Repository[User]):
    def __init__(self, database):
        self.Model = User
        super().__init__(database)

    def update_username(self, user: User, username: str):
        user.set_username(username)
        self._session.commit()

    def update_node_id(self, user: User, node_id: str):
        user.set_node_id(node_id)
        self._session.commit()

    def remove_node_id(self, user: User):
        user.remove_node_id()
        self._session.commit()
