from sqlalchemy.exc import NoResultFound

from ring_of_fire_bot.model.ring import Ring
from ring_of_fire_bot.model.ring_status import RING_STATUS
from ring_of_fire_bot.model.user import User
from ring_of_fire_bot.repository.i_ring_repository import IRingRepository


class RingRepository(IRingRepository):
    def __init__(self, database):
        self.Model = Ring
        super().__init__(database)

    def get_rings_by_ring_manager(self, ring_manager_id) -> [Ring]:
        result = self._new_query() \
            .filter(Ring.ring_manager.has(User.user_id == ring_manager_id)) \
            .filter(Ring.status != RING_STATUS.FINISHED.value) \
            .all()
        if not result:
            raise NoResultFound("No result was found.")
        return result

    def get_ring_by_chat_id(self, chat_id) -> Ring:
        result = self._new_query().filter(Ring.chat_id == chat_id).first()
        if not result:
            raise NoResultFound("No result was found.")
        return result

    def remove_user(self, ring: Ring, user: User) -> Ring:
        user_in_ring = self.find_user_in_ring(ring, user)
        ring.users.remove(user_in_ring)
        return ring





