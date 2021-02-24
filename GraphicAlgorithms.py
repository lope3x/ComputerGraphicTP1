from Point import Point


class GraphicAlgorithms:

    def __init__(self, drawPixel):
        self.drawPixel = drawPixel

    def dda(self, point1, point2):
        x1 = point1.x
        y1 = point1.y
        x2 = point2.x
        y2 = point2.y
        dx = x2 - x1
        dy = y2 - y1
        steps = 0
        if abs(dx) > abs(dy):
            steps = abs(dx)
        else:
            steps = abs(dy)
        x_incr = dx / steps
        y_incr = dy / steps
        x = x1
        y = y1
        self.drawPixel(round(x), round(y))
        for k in range(1, steps):
            x = x + x_incr
            y = y + y_incr
            self.drawPixel(round(x), round(y))

    def bresenhamDrawLine(self, point1, point2):
        x1 = point1.x
        y1 = point1.y
        x2 = point2.x
        y2 = point2.y
        dx = x2 - x1
        dy = y2 - y1
        incrx = 0
        incry = 0
        if dx >= 0:
            incrx = 1
        else:
            incrx = -1
            dx = -dx
        if dy >= 0:
            incry = 1
        else:
            incry = -1
            dy = -dy
        x = x1
        y = y1
        self.drawPixel(x, y)

        if dy < dx:
            p = 2 * dy - dx
            const1 = 2 * dy
            const2 = 2 * (dy - dx)
            for i in range(dx):
                x += incrx
                if p < 0:
                    p += const1
                else:
                    y += incry
                    p += const2
                self.drawPixel(x, y)
        else:
            p = 2 * dx - dy
            const1 = 2 * dx
            const2 = 2 * (dx - dy)
            for i in range(dy):
                y += incry
                if p < 0:
                    p += const1
                else:
                    x += incrx
                    p += const2
                self.drawPixel(x, y)

    def bresenhamDrawCircle(self, point, radius):
        xc = point.x
        yc = point.y

        def plotCirclePoints(x, y):
            self.drawPixel(xc + x, yc + y)
            self.drawPixel(xc - x, yc + y)
            self.drawPixel(xc + x, yc - y)
            self.drawPixel(xc - x, yc - y)
            self.drawPixel(xc + y, yc + x)
            self.drawPixel(xc - y, yc + x)
            self.drawPixel(xc + y, yc - x)
            self.drawPixel(xc - y, yc - x)

        x = 0
        y = radius
        p = 3 - 2 * radius
        plotCirclePoints(x, y)
        while x < y:
            if p < 0:
                p = p + 4 * x + 6
            else:
                p = p + 4 * (x - y) + 10
                y -= 1
            x += 1
            plotCirclePoints(x, y)


if __name__ == '__main__':
    pass
