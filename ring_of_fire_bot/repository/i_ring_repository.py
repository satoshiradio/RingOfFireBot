from ring_of_fire_bot.model.ring import Ring
from ring_of_fire_bot.model.user import User
from ring_of_fire_bot.repository.repository import Repository


class IRingRepository(Repository[Ring]):
    def __init__(self, database):
        self.Model = Ring
        super().__init__(database)

    def get_rings_by_ring_manager(self, ring_manager_id) -> [Ring]:
        raise NotImplementedError

    def get_ring_by_chat_id(self, chat_id) -> Ring:
        raise NotImplementedError

    def remove_user(self, ring: Ring, user: User) -> Ring:
        raise NotImplementedError

    def get_ring(self, message: str, chat_id: int) -> Ring:
        raise NotImplementedError
