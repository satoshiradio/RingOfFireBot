from sqlalchemy.exc import NoResultFound

from ring_of_fire_bot.model.ring import Ring
from ring_of_fire_bot.model.user import User
from ring_of_fire_bot.model.user_in_ring import UserInRing
from ring_of_fire_bot.repository.i_user_in_ring_repository import IUserInRingRepository


class UserInRingRepository(IUserInRingRepository):
    def __init__(self, database):
        self.Model = User
        super().__init__(database)

    def find_user_in_ring(self, ring: Ring, user: User) -> UserInRing:
        result = self._session \
            .query(UserInRing) \
            .filter(UserInRing.user_id == user.user_id) \
            .filter(UserInRing.ring_id == ring.ring_id).first()
        if not result:
            raise NoResultFound("No result was found.")
        return result
