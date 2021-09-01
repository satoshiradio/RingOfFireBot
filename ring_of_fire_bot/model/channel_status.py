from ring_of_fire_bot.utils.ExtendedEnum import ExtendedEnum


class CHANNEL_STATUS(ExtendedEnum):
    NOT_OPEN = "Channel not opened"
    PENDING = "Channel opening pending"
    OPEN = "Channel established"
