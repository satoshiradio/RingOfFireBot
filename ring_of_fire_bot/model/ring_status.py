from enum import Enum


class ExtendedEnum(Enum):
    @classmethod
    def list(cls):
        return list(map(lambda c: c, cls))


class STATUS(ExtendedEnum):
    WAITING_ON_PARTICIPANTS = "Waiting on participants to join"
    OPENING_CHANNELS = "Opening channels"
    BALANCING = "Balancing channels"
    FINISHED = "Ring is finished"
