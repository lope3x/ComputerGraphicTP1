import math
from math import cos, sin

from Metrics import Metrics
from Geometry import *


class GraphicAlgorithms:

    def __init__(self, draw_pixel):
        self.draw_pixel = draw_pixel

    def draw_dda_line(self, point1, point2):
        x1, x2, y1, y2 = self.unwrap_points(point1, point2)
        dx = x2 - x1
        dy = y2 - y1
        if abs(dx) > abs(dy):
            steps = abs(dx)
        else:
            steps = abs(dy)
        x_increment = dx / steps
        y_increment = dy / steps
        x = x1
        y = y1
        self.draw_pixel(round(x), round(y))
        for k in range(1, steps):
            x = x + x_increment
            y = y + y_increment
            self.draw_pixel(round(x), round(y))

    def draw_bresenham_line(self, point1, point2):
        x1, x2, y1, y2 = self.unwrap_points(point1, point2)
        dx = x2 - x1
        dy = y2 - y1

        if dx >= 0:
            x_increment = 1
        else:
            x_increment = -1
            dx = -dx
        if dy >= 0:
            y_increment = 1
        else:
            y_increment = -1
            dy = -dy
        x = x1
        y = y1
        self.draw_pixel(x, y)

        if dy < dx:
            p = 2 * dy - dx
            const1 = 2 * dy
            const2 = 2 * (dy - dx)
            for i in range(dx):
                x += x_increment
                if p < 0:
                    p += const1
                else:
                    y += y_increment
                    p += const2
                self.draw_pixel(x, y)
        else:
            p = 2 * dx - dy
            const1 = 2 * dx
            const2 = 2 * (dx - dy)
            for i in range(dy):
                y += y_increment
                if p < 0:
                    p += const1
                else:
                    x += x_increment
                    p += const2
                self.draw_pixel(x, y)

    def draw_bresenham_circle(self, point, radius):
        xc = point.x
        yc = point.y

        def draw_circle_points(x, y):
            self.draw_pixel(xc + x, yc + y)
            self.draw_pixel(xc - x, yc + y)
            self.draw_pixel(xc + x, yc - y)
            self.draw_pixel(xc - x, yc - y)
            self.draw_pixel(xc + y, yc + x)
            self.draw_pixel(xc - y, yc + x)
            self.draw_pixel(xc + y, yc - x)
            self.draw_pixel(xc - y, yc - x)

        x = 0
        y = radius
        p = 3 - 2 * radius
        draw_circle_points(x, y)
        while x < y:
            if p < 0:
                p = p + 4 * x + 6
            else:
                p = p + 4 * (x - y) + 10
                y -= 1
            x += 1
            draw_circle_points(x, y)

    def compute_clipped_line_cohen_sutherland(self, point1, point2, xmin, ymin, xmax, ymax):
        x1, x2, y1, y2 = self.unwrap_points(point1, point2)

        def compute_region_code(x, y):
            code = 0
            if x < xmin:
                code += 1
            if x > xmax:
                code += 2
            if y < ymin:
                code += 4
            if y > ymax:
                code += 8
            return code

        def get_bit_value_at_position(value, bit_position):
            bit_value = [1, 2, 4, 8]
            return 1 if (value & bit_value[bit_position] == bit_value[bit_position]) else 0

        accepted = False
        done = False
        while not done:
            c1 = compute_region_code(x1, y1)
            c2 = compute_region_code(x2, y2)
            if c1 == 0 and c2 == 0:
                accepted = True
                done = True
            elif c1 & c2 != 0:
                done = True
            else:
                if c1 != 0:
                    cfora = c1
                else:
                    cfora = c2
                if get_bit_value_at_position(cfora, 0) == 1:
                    xint = xmin
                    yint = y1 + (y2 - y1) * (xmin - x1) / (x2 - x1)
                elif get_bit_value_at_position(cfora, 1) == 1:
                    xint = xmax
                    yint = y1 + (y2 - y1) * (xmax - x1) / (x2 - x1)
                elif get_bit_value_at_position(cfora, 2) == 1:
                    yint = ymin
                    xint = x1 + (x2 - x1) * (ymin - y1) / (y2 - y1)
                elif get_bit_value_at_position(cfora, 3) == 1:
                    yint = ymax
                    xint = x1 + (x2 - x1) * (ymax - y1) / (y2 - y1)
                if c1 == cfora:
                    x1 = xint
                    y1 = yint
                else:
                    x2 = xint
                    y2 = yint
        if accepted:
            return round(x1), round(y1), round(x2), round(y2)

    u1 = 0.0
    u2 = 1.0

    def compute_clipped_line_liang_barsky(self, point1, point2, xmin, ymin, xmax, ymax):
        x1, x2, y1, y2 = self.unwrap_points(point1, point2)

        def clip_test(p, q):
            result = True
            if p < 0.0:
                r = q / p
                if r > self.u2:
                    result = False
                elif r > self.u1:
                    self.u1 = r
            elif p > 0.0:
                r = q / p
                if r < self.u1:
                    result = False
                elif r < self.u2:
                    self.u2 = r
            elif q < 0.0:
                result = False
            return result

        dx = x2 - x1
        dy = y2 - y1
        if clip_test(-dx, x1 - xmin):
            if clip_test(dx, xmax - x1):
                if clip_test(-dy, y1 - ymin):
                    if clip_test(dy, ymax - y1):
                        if self.u2 < 1.0:
                            x2 = x1 + self.u2 * dx
                            y2 = y1 + self.u2 * dy
                        if self.u1 > 0.0:
                            x1 = x1 + self.u1 * dx
                            y1 = y1 + self.u1 * dy
                        self.u1 = 0.0
                        self.u2 = 1.0
                        return round(x1), round(y1), round(x2), round(y2)
        self.u1 = 0.0
        self.u2 = 1.0

    @staticmethod
    def unwrap_points(point1, point2):
        x1 = point1.x
        y1 = point1.y
        x2 = point2.x
        y2 = point2.y
        return x1, x2, y1, y2

    @staticmethod
    def compute_distance_between_two_points(point1, point2):
        return math.sqrt(math.pow(point2.x - point1.x, 2) + math.pow(point2.y - point1.y, 2))

    @staticmethod
    def get_scaled_object(geometry_object, value, dim):
        if geometry_object.type == GeometryType.bresenhamCircle:
            radius = round(geometry_object.radius * value)
            return GeometryObject(geometry_object.type, point1=geometry_object.point1, radius=radius)
        if dim == "x":
            center_x, center_y = GraphicAlgorithms.get_line_center(geometry_object)

            point1_x = round((geometry_object.point1.x - center_x) * value) + center_x
            point2_x = (round((geometry_object.point2.x - center_x) * value)) + center_x

            point1 = Point(point1_x, geometry_object.point1.y)
            point2 = Point(point2_x, geometry_object.point2.y)
        else:
            center_x, center_y = GraphicAlgorithms.get_line_center(geometry_object)

            point1_y = round((geometry_object.point1.y - center_y) * value) + center_y
            point2_y = (round((geometry_object.point2.y - center_y) * value)) + center_y

            point1 = Point(geometry_object.point1.x, point1_y)
            point2 = Point(geometry_object.point2.x, point2_y)

        return GeometryObject(geometry_object.type, point1, point2)

    @staticmethod
    def get_rotated_geometry_object(geometry_object, angle):
        if geometry_object.type == GeometryType.bresenhamCircle:
            return geometry_object
        center_x, center_y = GraphicAlgorithms.get_line_center(geometry_object)
        x1, x2, y1, y2 = GraphicAlgorithms.unwrap_points(geometry_object.point1, geometry_object.point2)
        x1 = x1 - center_x
        x2 = x2 - center_x
        y1 = y1 - center_y
        y2 = y2 - center_y
        radians = math.radians(angle)
        point1_x = round(x1*cos(radians) - y1*sin(radians))
        point1_y = round(x1*sin(radians) + y1*cos(radians))

        point2_x = round(x2*cos(radians) - y2*sin(radians))
        point2_y = round(x2*sin(radians) + y2*cos(radians))

        point1_x = point1_x + center_x
        point1_y = point1_y + center_y

        point2_x = point2_x + center_x
        point2_y = point2_y + center_y

        point1 = Point(point1_x, point1_y)
        point2 = Point(point2_x, point2_y)

        return GeometryObject(geometry_object.type, point1, point2)


    @staticmethod
    def get_line_center(geometry_object):
        center_x = round((geometry_object.point1.x + geometry_object.point2.x) / 2)
        center_y = round((geometry_object.point1.y + geometry_object.point2.y) / 2)
        return center_x, center_y

    @staticmethod
    def get_translated_geometry_object(geometry_object, value, dim):
        if geometry_object.type == GeometryType.bresenhamCircle:
            if dim == "x":
                point1 = Point(geometry_object.point1.x + value, geometry_object.point1.y)
            else:
                point1 = Point(geometry_object.point1.x, geometry_object.point1.y + value)
            return GeometryObject(geometry_object.type, point1, radius=geometry_object.radius)
        else:
            if dim == "x":
                point1 = Point(geometry_object.point1.x + value, geometry_object.point1.y)
                point2 = Point(geometry_object.point2.x + value, geometry_object.point2.y)
            else:
                point1 = Point(geometry_object.point1.x, geometry_object.point1.y + value)
                point2 = Point(geometry_object.point2.x, geometry_object.point2.y + value)
            return GeometryObject(geometry_object.type, point1, point2)


if __name__ == '__main__':
    pass
