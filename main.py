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
        self.window.geometry(f"{GetSystemMetrics(0)}x{GetSystemMetrics(1)}")
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
                                     command=self.handleOnClickCleanScreen,
                                     padx=Metrics.paddingMenuButtonsX,
                                     pady=Metrics.paddingMenuButtonsY,
                                     ).pack()

    def handleOnClickMenuButton(self, algorithm):
        self.command = algorithm
        self.cleanPoints()

    def handleOnClickCleanScreen(self):
        self.canvas.delete("all")
        self.geometryObjects.clear()

    def cleanToggledButtons(self):
        self.ddaButton.btn.config(relief="raise")
        self.bresenamLineButton.btn.config(relief="raise")
        self.bresenamCircleButton.btn.config(relief="raise")
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
                print("First",self.firstPoint.x, self.firstPoint.y)
                print("Second",self.secondPoint.x, self.secondPoint.y)

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
