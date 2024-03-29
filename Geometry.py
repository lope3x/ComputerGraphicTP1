from enum import Enum


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class GeometryObject:
    def __init__(self, type_object, point1, point2=None, radius=None):
        self.type = type_object
        self.point1 = point1
        self.point2 = point2
        self.radius = radius


class GeometryType(Enum):
    ddd_Line = 0
    bresenham_Line = 1
    bresenham_Circle = 2


class ReflectionType(Enum):
    x_axis = 0
    y_axis = 1
    both_axis = 2
