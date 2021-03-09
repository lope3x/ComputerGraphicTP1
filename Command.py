from enum import Enum


class Command(Enum):
    NONE = 0
    DDA_LINE = 1
    BRESENHAM_LINE = 2
    BRESENHAM_CIRCLE = 3
    COHEN_SUTHERLAND_CLIP = 4
    LIANG_BARSKY_CLIP = 5
