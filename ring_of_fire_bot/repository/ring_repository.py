from sqlalchemy.exc import NoResultFound

from ring_of_fire_bot.model.channel_status import CHANNEL_STATUS
from ring_of_fire_bot.model.ring import Ring
from ring_of_fire_bot.model.ring_status import RING_STATUS
from ring_of_fire_bot.model.user import User
from ring_of_fire_bot.model.user_in_ring import UserInRing
from ring_of_fire_bot.repository.generic import Repository


class RingRepository(Repository[Ring]):
    def __init__(self, database):
        self.Model = Ring
        super().__init__(database)

    def get_rings_by_ring_manager(self, ring_manager_id):
        result = self._new_query() \
            .filter(Ring.ring_manager.has(User.user_id == ring_manager_id)) \
            .filter(Ring.status != RING_STATUS.FINISHED.value) \
            .all()
        if not result:
            raise NoResultFound("No result was found.")
        return result

    def get_ring_by_chat_id(self, chat_id):
        result = self._new_query().filter(Ring.chat_id == chat_id).first()
        if not result:
            raise NoResultFound("No result was found.")
        return result

    def update_ring_status(self, ring: Ring, status: RING_STATUS):
        ring.set_status(status)
        self._session.commit()

    def set_channel_size(self, ring: Ring, channel_size: int):
        ring.set_channel_size(channel_size)
        self._session.commit()

    def set_max_members(self, ring: Ring, max_members: int):
        ring.set_max_ring_members(max_members)
        self._session.commit()

    def add_member_to_ring(self, ring: Ring, user_in_ring: UserInRing):
        ring.add_member(user_in_ring)
        self._session.commit()

    def set_chat_id(self, ring: Ring, chat_id: int):
        ring.set_chat_id(chat_id)
        self._session.commit()

    def remove_chat_id(self, ring: Ring):
        ring.remove_chat_id()
        self._session.commit()

    def find_user_in_ring(self, ring: Ring, user: User):
        result = self._session \
            .query(UserInRing) \
            .filter(UserInRing.user_id == user.user_id) \
            .filter(UserInRing.ring_id == ring.ring_id).first()
        if not result:
            raise NoResultFound("No result was found.")
        return result

    def remove_user(self, ring: Ring, user: User):
        user_in_ring = self.find_user_in_ring(ring, user)
        ring.users.remove(user_in_ring)
        self._session.commit()

    def update_channel_status(self, ring: Ring, user: User, channel_status: CHANNEL_STATUS):
        user_in_ring: UserInRing = self.find_user_in_ring(ring, user)
        user_in_ring.channel_status = channel_status
        self._session.commit()

    def update_funded(self, ring: Ring, user: User, funded: bool):
        user_in_ring: UserInRing = self.find_user_in_ring(ring, user)
        user_in_ring.is_funded = funded
        self._session.commit()
