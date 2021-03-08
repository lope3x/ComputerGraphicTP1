import math
import tkinter as tk

from Command import Command
from GraphicAlgorithms import GraphicAlgorithms
from Metrics import Metrics
from Geometry import *
from ToggleButton import ToggleButton
from win32api import GetSystemMetrics


class MainGui:

    def __init__(self):
        # Screen
        self.window = tk.Tk()
        # self.window.geometry(f"{GetSystemMetrics(0)}x{GetSystemMetrics(1)}")
        self.window.geometry(f"{600}x{600}")
        self.configureWidgets()
        self.events()

        # Variables
        self.numberOfClicks = 0
        self.command = Command.NONE
        self.ga = GraphicAlgorithms(self.drawPixelAt)
        self.firstPoint = None
        self.secondPoint = None
        self.geometryObjects = []

        self.canvas.pack()
        self.window.mainloop()

    def configureWidgets(self):
        self.configureMenu()
        self.canvas = tk.Canvas(self.window,
                                bg="white",
                                width=GetSystemMetrics(0),
                                height=GetSystemMetrics(1))
        self.canvas.pack()

    def configureMenu(self):
        self.menuFrame = tk.Frame(self.window)
        self.configureMenuButtons()
        self.menuFrame.pack()

    def configureMenuButtons(self):
        self.ddaButton = ToggleButton(self.menuFrame,
                                      text="DDA",
                                      command=self.handleOnClickMenuButton,
                                      algorithm=Command.DDA,
                                      cleanButtons=self.cleanToggledButtons)
        self.bresenamLineButton = ToggleButton(self.menuFrame,
                                               text="BresenhamLine",
                                               command=self.handleOnClickMenuButton,
                                               algorithm=Command.BRESENHAMLINE,
                                               cleanButtons=self.cleanToggledButtons)
        self.bresenamCircleButton = ToggleButton(self.menuFrame,
                                                 text="BresenhamCircle",
                                                 command=self.handleOnClickMenuButton,
                                                 algorithm=Command.BRESENHAMCIRCLE,
                                                 cleanButtons=self.cleanToggledButtons)
        self.cohenSutherlandButton = ToggleButton(self.menuFrame,
                                                  text="Recorte CS",
                                                  command=self.handleOnClickMenuButton,
                                                  algorithm=Command.COHENSUTHERLAND,
                                                  cleanButtons=self.cleanToggledButtons)
        self.cleanButton = tk.Button(self.menuFrame,
                                     text="Clean Screen",
                                     width=Metrics.buttonSize,
                                     relief="raised",
                                     command=self.cleanScreen,
                                     padx=Metrics.paddingMenuButtonsX,
                                     pady=Metrics.paddingMenuButtonsY,
                                     ).pack()

    def handleOnClickMenuButton(self, algorithm):
        self.command = algorithm
        self.cleanPoints()

    def cleanScreen(self):
        self.canvas.delete("all")
        self.geometryObjects.clear()

    def reRenderScreen(self):
        for geometryObject in self.geometryObjects:
            if geometryObject.type == GeometryType.dddLine:
                self.ga.dda(geometryObject.point1, geometryObject.point2)
            elif geometryObject.type == GeometryType.bresenhamLine:
                self.ga.bresenhamDrawLine(geometryObject.point1, geometryObject.point2)
            else:
                self.ga.bresenhamDrawCircle(geometryObject.point1, geometryObject.radius)

    def cleanToggledButtons(self):
        self.ddaButton.btn.config(relief="raise")
        self.bresenamLineButton.btn.config(relief="raise")
        self.bresenamCircleButton.btn.config(relief="raise")
        self.cohenSutherlandButton.btn.config(relief="raise")
        self.command = Command.NONE

    def drawPixelAt(self, x, y):
        # self.canvas.create_rectangle((x,y)*2)
        self.canvas.create_line(x, y, x + 1, y)

    def events(self):
        # self.canvas.bind('<B1-Motion>', lambda event: self.drawPixelAt(event.x, event.y))
        self.canvas.bind('<ButtonRelease-1>', lambda event: self.handleOnClickScreen(Point(event.x, event.y)))

    def handleOnClickScreen(self, point):
        if self.command != Command.NONE:
            if self.firstPoint is None:
                self.firstPoint = point
            else:
                self.secondPoint = point

        if self.shouldDrawOnScreen():
            if self.command == Command.DDA:
                ddaLine = GeometryObject(GeometryType.dddLine, self.firstPoint, self.secondPoint)
                self.geometryObjects.append(ddaLine)
                self.ga.dda(self.firstPoint, self.secondPoint)
            elif self.command == Command.BRESENHAMLINE:
                bresenhamLine = GeometryObject(GeometryType.bresenhamLine, self.firstPoint, self.secondPoint)
                self.geometryObjects.append(bresenhamLine)
                self.ga.bresenhamDrawLine(self.firstPoint, self.secondPoint)
            elif self.command == Command.BRESENHAMCIRCLE:
                radius = self.distanceBetweenTwoPoints(self.firstPoint, self.secondPoint)
                bresenhamCircle = GeometryObject(GeometryType.bresenhamCircle, self.firstPoint, radius=radius)
                self.geometryObjects.append(bresenhamCircle)
                self.ga.bresenhamDrawCircle(self.firstPoint, radius)
            elif self.command == Command.COHENSUTHERLAND:
                xmin = self.firstPoint.x if self.firstPoint.x < self.secondPoint.x else self.secondPoint.x
                ymin = self.firstPoint.y if self.firstPoint.y < self.secondPoint.y else self.secondPoint.y
                xmax = self.firstPoint.x if self.firstPoint.x > self.secondPoint.x else self.secondPoint.x
                ymax = self.firstPoint.y if self.firstPoint.y > self.secondPoint.y else self.secondPoint.y
                newGeometryObjectList = []
                for geometryObject in self.geometryObjects:
                    try:
                        if geometryObject.type == GeometryType.dddLine:
                            x1, y1, x2, y2 = self.ga.cohen_sutherland(geometryObject.point1, geometryObject.point2,
                                                                      xmin, ymin, xmax, ymax)
                            point1 = Point(x1, y1)
                            point2 = Point(x2, y2)
                            newGeometryObject = GeometryObject(GeometryType.dddLine, point1, point2)
                            newGeometryObjectList.append(newGeometryObject)
                        elif geometryObject.type == GeometryType.bresenhamLine:
                            x1, y1, x2, y2 = self.ga.cohen_sutherland(geometryObject.point1, geometryObject.point2,
                                                                      xmin, ymin, xmax, ymax)
                            point1 = Point(x1, y1)
                            point2 = Point(x2, y2)
                            newGeometryObject = GeometryObject(GeometryType.bresenhamLine, point1, point2)
                            newGeometryObjectList.append(newGeometryObject)
                    except:
                        print("é isso n ta legal ")
                        pass
                self.cleanScreen()
                self.geometryObjects = newGeometryObjectList
                self.reRenderScreen()
            elif self.command == Command.NONE:
                pass
            self.cleanPoints()

    def shouldDrawOnScreen(self):
        return self.firstPoint is not None and \
               self.secondPoint is not None and \
               self.command != Command.NONE

    def cleanPoints(self):
        self.firstPoint = self.secondPoint = None

    def distanceBetweenTwoPoints(self, point1, point2):
        return math.sqrt(math.pow(point2.x - point1.x, 2) + math.pow(point2.y - point1.y, 2))


def main():
    mg = MainGui()


if __name__ == '__main__':
    main()
