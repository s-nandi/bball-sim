from enum import Enum, auto


class BallMode(Enum):
    HELD = auto()
    MIDPASS = auto()
    RECEIVEDPASS = auto()
    MIDSHOT = auto()
    REACHEDSHOT = auto()
    DEAD = auto()
