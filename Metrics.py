from win32api import GetSystemMetrics


class Metrics:
    buttonSize = 15
    paddingMenuButtonsX = 5
    paddingMenuButtonsY = 5
    canvas_width = GetSystemMetrics(0)
    canvas_height = GetSystemMetrics(1)