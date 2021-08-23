from sqlalchemy.exc import NoResultFound

from ring_of_fire_bot.model.Exceptions.invalid_node_key_exception import InvalidNodeKeyException
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

    # can only be used if the only argument is the ring_id
    def get_ring(self, message: str, chat_id: int) -> Ring:
        split_message = message.split(' ')
        # if ring_id is provided find ring with that ID
        if len(split_message) < 2:
            # no ring provided
            ring = self.get_ring_by_chat_id(chat_id)
            if ring:
                return ring
            else:
                raise InvalidNodeKeyException
        # check if chat has a ring
        else:
            ring_id = int(split_message[1])
            return self.get(ring_id)





