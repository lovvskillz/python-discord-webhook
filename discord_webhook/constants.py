from enum import Enum


class MessageFlags(Enum):
    NONE = 0
    SUPPRESS_EMBEDS = 4
    SUPPRESS_NOTIFICATIONS = 4096
