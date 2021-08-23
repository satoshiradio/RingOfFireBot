from ring_of_fire_bot.model.ring import Ring
from ring_of_fire_bot.model.user import User
from ring_of_fire_bot.model.user_in_ring import UserInRing
from ring_of_fire_bot.repository.repository import Repository


class IUserInRingRepository(Repository[UserInRing]):
    pass

    def find_user_in_ring(self, ring: Ring, user: User) -> UserInRing:
        raise NotImplementedError

