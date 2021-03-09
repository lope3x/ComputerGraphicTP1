import math
import tkinter as tk
from tkinter import simpledialog

from Command import Command
from GraphicAlgorithms import GraphicAlgorithms
from Metrics import Metrics
from Geometry import *
from ToggleButton import ToggleButton
from win32api import GetSystemMetrics


# noinspection PyAttributeOutsideInit
class MainGui:

    def __init__(self):
        # Screen
        self.window = tk.Tk()
        # self.window.geometry(f"{GetSystemMetrics(0)}x{GetSystemMetrics(1)}")
        self.window.geometry(f"{1000}x{600}")
        self.window.title("Paint")
        self.configure_widgets()
        self.bind_events()

        # Variables
        self.numberOfClicks = 0
        self.command = Command.NONE
        self.ga = GraphicAlgorithms(self.draw_pixel_at)
        self.firstPoint = None
        self.secondPoint = None
        self.geometry_objects_list = []
        self.temporary_geometry_object_list = []
        self.dim = None

        self.canvas.pack()
        self.window.mainloop()

    def configure_widgets(self):
        self.configure_menu()
        self.canvas = tk.Canvas(self.window,
                                bg="white",
                                width=1000,
                                height=570)
        self.canvas.pack()

    def configure_menu(self):
        self.menu_frame = tk.Frame(self.window)
        self.configure_menu_buttons()
        self.menu_frame.pack()

    def configure_menu_buttons(self):
        self.dda_button = ToggleButton(self.menu_frame,
                                       text="DDA",
                                       command=self.handle_on_click_menu_button,
                                       algorithm=Command.DDA_LINE,
                                       clean_buttons=self.clean_toggled_buttons)
        self.bresenham_line_button = ToggleButton(self.menu_frame,
                                                  text="BresenhamLine",
                                                  command=self.handle_on_click_menu_button,
                                                  algorithm=Command.BRESENHAM_LINE,
                                                  clean_buttons=self.clean_toggled_buttons)
        self.bresenham_circle_button = ToggleButton(self.menu_frame,
                                                    text="BresenhamCircle",
                                                    command=self.handle_on_click_menu_button,
                                                    algorithm=Command.BRESENHAM_CIRCLE,
                                                    clean_buttons=self.clean_toggled_buttons)
        self.cohen_sutherland_button = ToggleButton(self.menu_frame,
                                                    text="Recorte CS",
                                                    command=self.handle_on_click_menu_button,
                                                    algorithm=Command.COHEN_SUTHERLAND_CLIP,
                                                    clean_buttons=self.clean_toggled_buttons)
        self.liang_barsky_button = ToggleButton(self.menu_frame,
                                                text="Recorte LB",
                                                command=self.handle_on_click_menu_button,
                                                algorithm=Command.LIANG_BARSKY_CLIP,
                                                clean_buttons=self.clean_toggled_buttons)
        self.translation_button = tk.Button(self.menu_frame,
                                            text="Translação",
                                            width=Metrics.buttonSize,
                                            relief="raised",
                                            command=self.handle_on_click_translation_button,
                                            padx=Metrics.paddingMenuButtonsX,
                                            pady=Metrics.paddingMenuButtonsY,
                                            ).pack(side="left")
        self.scaling_button = tk.Button(self.menu_frame,
                                        text="Escala",
                                        width=Metrics.buttonSize,
                                        relief="raised",
                                        command=self.handle_on_click_scaling_button,
                                        padx=Metrics.paddingMenuButtonsX,
                                        pady=Metrics.paddingMenuButtonsY,
                                        ).pack(side="left")
        self.clean_button = tk.Button(self.menu_frame,
                                      text="Clean Screen",
                                      width=Metrics.buttonSize,
                                      relief="raised",
                                      command=self.clean_screen,
                                      padx=Metrics.paddingMenuButtonsX,
                                      pady=Metrics.paddingMenuButtonsY,
                                      ).pack()

    def handle_on_click_confirm_scaling(self, scaling_dialog):
        scaling_dialog.destroy()
        self.dim = None
        self.render_geometry_objects_list_on_screen_and_overwrite_old_list(list(self.temporary_geometry_object_list))

    def handle_on_slider_scaling_slide(self, value, dim):
        if self.dim is None:
            self.dim = dim
        elif self.dim != dim:
            self.dim = dim
            self.geometry_objects_list = list(self.temporary_geometry_object_list)
        if len(self.temporary_geometry_object_list) != len(self.geometry_objects_list):
            self.temporary_geometry_object_list = [0 for _ in range(0, len(self.geometry_objects_list))]
        for i in range(0, len(self.geometry_objects_list)):
            geometry_object = self.geometry_objects_list[i]
            scaled_geometry_object = self.get_scaled_object(geometry_object, float(value), dim)
            self.temporary_geometry_object_list[i] = scaled_geometry_object
        self.canvas.delete("all")
        self.render_geometry_objects_on_screen(self.temporary_geometry_object_list)

    def get_scaled_object(self, geometry_object, value, dim):
        if geometry_object.type == GeometryType.bresenhamCircle:
            radius = round(geometry_object.radius*value)
            return GeometryObject(geometry_object.type, point1=geometry_object.point1, radius=radius)
        if dim == "x":
            point1 = Point(round(geometry_object.point1.x * value), geometry_object.point1.y)
            point2 = Point(round(geometry_object.point2.x * value), geometry_object.point2.y)
        else:
            point1 = Point(geometry_object.point1.x, round(geometry_object.point1.y * value))
            point2 = Point(geometry_object.point2.x, round(geometry_object.point2.y * value))

        return GeometryObject(geometry_object.type, point1, point2)

    def handle_on_click_scaling_button(self):
        scaling_dialog = tk.Toplevel(self.window)
        scaling_dialog.title("Escala")
        scaling_dialog.geometry("200x200")
        tk.Label(scaling_dialog,
                 text="Ajuste o valor de escala abaixo").pack()
        tk.Label(scaling_dialog, text="Escala em X").pack()
        scale_x_slider = tk.Scale(scaling_dialog,
                                  from_=0.01,
                                  to=2,
                                  orient=tk.HORIZONTAL,
                                  length="200",
                                  resolution=0.01,
                                  command=lambda value: self.handle_on_slider_scaling_slide(value, "x"))
        scale_x_slider.set(1)
        scale_x_slider.pack()
        tk.Label(scaling_dialog, text="Escala em Y").pack()
        scale_y_slider = tk.Scale(scaling_dialog,
                                  from_=0.01,
                                  to=2,
                                  orient=tk.HORIZONTAL,
                                  length="200",
                                  resolution=0.01,
                                  command=lambda value: self.handle_on_slider_scaling_slide(value, "y"))
        scale_y_slider.set(1)
        scale_y_slider.pack()
        scale_button_done = tk.Button(scaling_dialog,
                                      text="Confirmar Escala",
                                      command=lambda: self.handle_on_click_confirm_scaling(scaling_dialog))

        scale_button_done.pack()

    def handle_on_click_translation_button(self):
        translation_dialog = tk.Toplevel(self.window)
        translation_dialog.title("Translação")
        translation_dialog.geometry("200x100")
        tk.Label(translation_dialog,
                 text="Digite os valores X e Y de translação").grid(row=0, columnspan=2)
        tk.Label(translation_dialog, text="X").grid(row=1)
        tk.Label(translation_dialog, text="Y").grid(row=2)
        x_entry = tk.Entry(translation_dialog)
        x_entry.grid(row=1, column=1)
        y_entry = tk.Entry(translation_dialog)
        y_entry.grid(row=2, column=1)
        tk.Button(translation_dialog,
                  text="Transladar",
                  command=lambda: self.handle_on_click_translation_dialog_submit(x_entry, y_entry)).grid(row=3,
                                                                                                         columnspan=2)

    def handle_on_click_translation_dialog_submit(self, x_entry, y_entry):
        x = int(x_entry.get())
        y = int(y_entry.get())
        self.translate_geometry_objects(x, y)

    def translate_geometry_objects(self, x, y):
        new_geometry_object_list = []
        for geometry_object in self.geometry_objects_list:
            new_geometry_object_list.append(self.get_translate_geometry_object(geometry_object, x, y))
        self.render_geometry_objects_list_on_screen_and_overwrite_old_list(new_geometry_object_list)

    def render_geometry_objects_list_on_screen_and_overwrite_old_list(self, new_geometry_object_list):
        self.clean_screen()
        self.geometry_objects_list = new_geometry_object_list
        self.render_geometry_objects_on_screen(self.geometry_objects_list)

    def get_translate_geometry_object(self, geometry_object, tx, ty):
        if geometry_object.type == GeometryType.bresenhamCircle:
            point1 = Point(geometry_object.point1.x + tx, geometry_object.point1.y + ty)
            return GeometryObject(geometry_object.type, point1, radius=geometry_object.radius)
        else:
            point1 = Point(geometry_object.point1.x + tx, geometry_object.point1.y + ty)
            point2 = Point(geometry_object.point2.x + tx, geometry_object.point2.y + ty)
            return GeometryObject(geometry_object.type, point1, point2)

    def handle_on_click_menu_button(self, algorithm):
        self.command = algorithm
        self.clean_click_points()

    def clean_screen(self):
        self.canvas.delete("all")
        self.geometry_objects_list.clear()
        self.temporary_geometry_object_list.clear()

    def render_geometry_objects_on_screen(self, geometry_objects_list):
        for geometryObject in geometry_objects_list:
            if geometryObject.type == GeometryType.dddLine:
                self.ga.draw_dda_line(geometryObject.point1, geometryObject.point2)
            elif geometryObject.type == GeometryType.bresenhamLine:
                self.ga.draw_bresenham_line(geometryObject.point1, geometryObject.point2)
            else:
                self.ga.draw_bresenham_circle(geometryObject.point1, geometryObject.radius)

    def clean_toggled_buttons(self):
        self.dda_button.btn.config(relief="raise")
        self.bresenham_line_button.btn.config(relief="raise")
        self.bresenham_circle_button.btn.config(relief="raise")
        self.cohen_sutherland_button.btn.config(relief="raise")
        self.liang_barsky_button.btn.config(relief="raise")
        self.command = Command.NONE

    def draw_pixel_at(self, x, y):
        self.canvas.create_line(x, y, x + 1, y)

    def bind_events(self):
        # self.canvas.bind('<B1-Motion>', lambda event: self.drawPixelAt(event.x, event.y))
        self.canvas.bind('<ButtonRelease-1>', lambda event: self.handle_on_click_screen(Point(event.x, event.y)))

    def handle_on_click_screen(self, point):
        if self.command != Command.NONE:
            if self.firstPoint is None:
                self.firstPoint = point
            else:
                self.secondPoint = point

        if self.should_draw_on_screen():
            if self.command == Command.DDA_LINE:
                self.handle_click_dda_line()
            elif self.command == Command.BRESENHAM_LINE:
                self.handle_click_bresenham_line()
            elif self.command == Command.BRESENHAM_CIRCLE:
                self.handle_click_bresenham_circle()
            elif self.command == Command.COHEN_SUTHERLAND_CLIP:
                self.handle_click_clip(Command.COHEN_SUTHERLAND_CLIP)
            elif self.command == Command.LIANG_BARSKY_CLIP:
                self.handle_click_clip(Command.LIANG_BARSKY_CLIP)
            elif self.command == Command.NONE:
                pass
            self.clean_click_points()

    def handle_click_clip(self, algorithm):
        new_geometry_object_list = []
        for geometry_object in self.geometry_objects_list:
            if geometry_object.type != GeometryType.bresenhamCircle:
                try:
                    new_geometry_object = self.compute_new_clipped_line(geometry_object, algorithm)
                    new_geometry_object_list.append(new_geometry_object)
                except:
                    pass
        self.render_geometry_objects_list_on_screen_and_overwrite_old_list(new_geometry_object_list)

    def compute_new_clipped_line(self, geometry_object, algorithm):
        x_max, x_min, y_max, y_min = self.get_clipping_limits()
        if algorithm == Command.COHEN_SUTHERLAND_CLIP:
            x1, y1, x2, y2 = self.ga.compute_clipped_line_cohen_sutherland(geometry_object.point1,
                                                                           geometry_object.point2,
                                                                           x_min, y_min, x_max,
                                                                           y_max)
        else:
            x1, y1, x2, y2 = self.ga.compute_clipped_line_liang_barsky(geometry_object.point1,
                                                                       geometry_object.point2,
                                                                       x_min, y_min, x_max,
                                                                       y_max)
        point1 = Point(x1, y1)
        point2 = Point(x2, y2)
        new_geometry_object = GeometryObject(geometry_object.type, point1, point2)
        return new_geometry_object

    def handle_click_bresenham_circle(self):
        radius = GraphicAlgorithms.compute_distance_between_two_points(self.firstPoint, self.secondPoint)
        bresenham_circle = GeometryObject(GeometryType.bresenhamCircle, self.firstPoint, radius=radius)
        self.geometry_objects_list.append(bresenham_circle)
        self.ga.draw_bresenham_circle(self.firstPoint, radius)

    def handle_click_bresenham_line(self):
        bresenham_line = GeometryObject(GeometryType.bresenhamLine, self.firstPoint, self.secondPoint)
        self.geometry_objects_list.append(bresenham_line)
        self.ga.draw_bresenham_line(self.firstPoint, self.secondPoint)

    def handle_click_dda_line(self):
        dda_line = GeometryObject(GeometryType.dddLine, self.firstPoint, self.secondPoint)
        self.geometry_objects_list.append(dda_line)
        self.ga.draw_dda_line(self.firstPoint, self.secondPoint)

    def get_clipping_limits(self):
        x_min = self.firstPoint.x if self.firstPoint.x < self.secondPoint.x else self.secondPoint.x
        y_min = self.firstPoint.y if self.firstPoint.y < self.secondPoint.y else self.secondPoint.y
        x_max = self.firstPoint.x if self.firstPoint.x > self.secondPoint.x else self.secondPoint.x
        y_max = self.firstPoint.y if self.firstPoint.y > self.secondPoint.y else self.secondPoint.y
        return x_max, x_min, y_max, y_min

    def should_draw_on_screen(self):
        return self.firstPoint is not None and \
               self.secondPoint is not None and \
               self.command != Command.NONE

    def clean_click_points(self):
        self.firstPoint = self.secondPoint = None


def main():
    mg = MainGui()


if __name__ == '__main__':
    main()
