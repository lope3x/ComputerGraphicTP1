from enum import Enum


class Command(Enum):
    NONE = 0
    DDA = 1
    BRESENHAMLINE = 2
    BRESENHAMCIRCLE = 3
    COHENSUTHERLAND = 4
    LIANGBARSKY = 5
