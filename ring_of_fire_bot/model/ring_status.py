from ring_of_fire_bot.utils.ExtendedEnum import ExtendedEnum


class RING_STATUS(ExtendedEnum):
    WAITING = "Waiting on participants to join"
    OPENING = "Opening channels"
    BALANCING = "Balancing channels"
    FINISHED = "Ring is finished"
