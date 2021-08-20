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

    def update_ring_status(self, ring_id, status: STATUS):
        ring = self.get(ring_id)
        ring.set_status(status)
        self._session.commit()

    def set_channel_size(self, ring_id, channel_size: int):
        ring = self.get(ring_id)
        ring.set_channel_size(channel_size)
        self._session.commit()

    def set_max_members(self, ring_id: int, max_members: int):
        ring = self.get(ring_id)
        ring.set_max_ring_members(max_members)
        self._session.commit()

    def add_member_to_ring(self, ring_id, user: User):
        ring = self.get(ring_id)
        ring.add_member(user)
        self._session.commit()
