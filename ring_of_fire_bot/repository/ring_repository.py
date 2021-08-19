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

    def add_member_to_ring(self, ring_id, user: User):
        ring = self.get(ring_id)
        ring.ring_members.append(user)
        self._session.commit()

    def update_ring_status(self, ring_id, status: STATUS):
        ring = self.get(ring_id)
        ring.status = status
        self._session.commit()
