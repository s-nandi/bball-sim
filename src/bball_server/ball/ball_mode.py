from enum import Enum, auto


class BallMode(Enum):
    HELD = auto()
    MIDPASS = auto()
    POSTPASS = auto()
    MIDSHOT = auto()
    POSTSHOT = auto()
    DEAD = auto()
