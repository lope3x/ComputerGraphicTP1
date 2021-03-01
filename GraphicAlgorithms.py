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

    xmin = -2
    xmax = 5
    ymin = 1
    ymax = 6

    def cohen_sutherland(self, x1, x2, y1, y2):
        def regionCode(x, y):
            code = 0
            if x < self.xmin:
                code += 1
            if x > self.xmax:
                code += 2
            if y < self.ymin:
                code += 4
            if y > self.ymax:
                code += 8
            return code

        def getBitValue(value, bit_position):
            bit_value = [1, 2, 4, 8]
            return 1 if (value & bit_value[bit_position] == bit_value[bit_position]) else 0

        aceite = False
        feito = False
        while not feito:
            c1 = regionCode(x1, y1)
            c2 = regionCode(x2, y2)
            if c1 == 0 and c2 == 0:
                aceite = True
                feito = True
            elif c1 & c2 != 0:
                feito = True
            else:
                if c1 != 0:
                    cfora = c1
                else:
                    cfora = c2
                if getBitValue(cfora, 0) == 1:
                    xint = self.xmin
                    yint = y1 + (y2 - y1) * (self.xmin - x1) / (x2 - x1)
                elif getBitValue(cfora, 1) == 1:
                    xint = self.xmax
                    yint = y1 + (y2 - y1) * (self.xmax - x1) / (x2 - x1)
                elif getBitValue(cfora, 2) == 1:
                    yint = self.ymin
                    xint = x1 + (x2 - x1) * (self.ymin - y1) / (y2 - y1)
                elif getBitValue(cfora, 3) == 1:
                    yint = self.ymax
                    xint = x1 + (x2 - x1) * (self.ymax - y1) / (y2 - y1)
                if c1 == cfora:
                    x1 = xint
                    y1 = yint
                else:
                    x2 = xint
                    y2 = yint
        if aceite:
            pass  # desenhar linha aqui


if __name__ == '__main__':
    pass
