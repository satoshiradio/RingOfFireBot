from enum import Enum


class STATUS(Enum):
    WAITING_ON_PARTICIPANTS = 0
    OPENING_CHANNELS = 1
    BALANCING = 2
    FINISHED = 3

