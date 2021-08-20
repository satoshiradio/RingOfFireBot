from ring_of_fire_bot.model.ring import Ring
from ring_of_fire_bot.model.ring_status import STATUS
from ring_of_fire_bot.model.user import User
from ring_of_fire_bot.repository.generic import Repository


class RingRepository(Repository[Ring]):
    def __init__(self, database):
        self.Model = Ring
        super().__init__(database)

    def get_rings_by_ring_manager(self, ring_manager_id):
        return self._new_query() \
            .filter(Ring.ring_manager.has(User.user_id == ring_manager_id)) \
            .filter(Ring.status != STATUS.FINISHED.value) \
            .all()

    def get_ring_by_chat_id(self, chat_id):
        print(chat_id)
        return self._new_query().filter(Ring.chat_id == chat_id).first()

    def update_ring_status(self, ring: Ring, status: STATUS):
        ring.set_status(status)
        self._session.commit()

    def set_channel_size(self, ring: Ring, channel_size: int):
        ring.set_channel_size(channel_size)
        self._session.commit()

    def set_max_members(self, ring: Ring, max_members: int):
        ring.set_max_ring_members(max_members)
        self._session.commit()

    def add_member_to_ring(self, ring: Ring, user: User):
        ring.add_member(user)
        self._session.commit()

    def set_chat_id(self, ring: Ring, chat_id: int):
        ring.set_chat_id(chat_id)
        self._session.commit()

    def remove_chat_id(self, ring: Ring):
        ring.remove_chat_id()
        self._session.commit()
