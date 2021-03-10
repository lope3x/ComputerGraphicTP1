import math
import tkinter as tk
from tkinter import simpledialog, messagebox, X

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
        self.window.geometry(f"{Metrics.canvas_width}x{600}")
        self.window.title("Paint")
        self.configure_widgets()
        self.bind_events()

        # Variables
        self.numberOfClicks = 0
        self.command = Command.NONE
        self.ga = GraphicAlgorithms(self.draw_pixel_at)
        self.firstPoint = None
        self.secondPoint = None
        self.clip_first_point = None
        self.clip_second_point = None
        self.geometry_objects_list = []
        self.temporary_geometry_object_list = []
        self.dim = None

        self.canvas.pack()
        self.window.mainloop()

    def configure_widgets(self):
        self.configure_menu()
        self.canvas = tk.Canvas(self.window,
                                bg="white",
                                width=Metrics.canvas_width,
                                height=Metrics.canvas_height)
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
        self.rotation_button = tk.Button(self.menu_frame,
                                         text="Rotação",
                                         width=Metrics.buttonSize,
                                         relief="raised",
                                         command=self.handle_on_click_rotation_button,
                                         padx=Metrics.paddingMenuButtonsX,
                                         pady=Metrics.paddingMenuButtonsY,
                                         ).pack(side="left")
        self.reflection_button = tk.Button(self.menu_frame,
                                           text="Reflexão",
                                           width=Metrics.buttonSize,
                                           relief="raised",
                                           command=self.handle_on_click_reflection_button,
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

    def handle_on_click_reflection_type_button(self, type):
        self.temporary_geometry_object_list = []
        for geometry_object in self.geometry_objects_list:
            if geometry_object.type != GeometryType.bresenham_Circle:
                reflected_object = GraphicAlgorithms.get_reflected_geometry_object(geometry_object, type)
                self.temporary_geometry_object_list.append(reflected_object)
        self.canvas.delete("all")
        self.render_geometry_objects_on_screen(list(self.temporary_geometry_object_list))

    def handle_on_click_reflection_button(self):
        if self.command != Command.NONE:
            messagebox.showerror(title="Error", message="Desmarque todos os botoes para utilizar este comando")
            return
        reflection_dialog = tk.Toplevel(self.window)
        reflection_dialog.title("Reflexão")
        reflection_dialog.geometry("200x130")
        tk.Label(reflection_dialog,
                 text="Selecione a reflexão desejada abaixo").pack()
        tk.Button(reflection_dialog,
                  text="Eixo X",
                  command=lambda: self.handle_on_click_reflection_type_button(ReflectionType.x_axis)).pack(fill=X)
        tk.Button(reflection_dialog,
                  text="Eixo Y",
                  command=lambda: self.handle_on_click_reflection_type_button(ReflectionType.y_axis)).pack(fill=X)
        tk.Button(reflection_dialog,
                  text="Ambos os Eixos",
                  command=lambda: self.handle_on_click_reflection_type_button(ReflectionType.both_axis)).pack(fill=X)

        tk.Button(reflection_dialog,
                  text="Confirmar Rotação",
                  command=lambda: self.handle_on_click_confirm_transformation(reflection_dialog)).pack(fill=X)

    def handle_on_click_rotation_button(self):
        if self.command != Command.NONE:
            messagebox.showerror(title="Error", message="Desmarque todos os botoes para utilizar este comando")
            return
        rotation_dialog = tk.Toplevel(self.window)
        rotation_dialog.title("Rotação")
        rotation_dialog.geometry("200x100")
        tk.Label(rotation_dialog,
                 text="Ajuste o valor de rotação abaixo").pack()
        rotation_slider = tk.Scale(rotation_dialog,
                                   from_=0,
                                   to=360,
                                   orient=tk.HORIZONTAL,
                                   length="200",
                                   command=lambda value: self.handle_on_slider_rotation_slide(value))
        rotation_slider.set(0)
        rotation_slider.pack()
        rotation_button_done = tk.Button(rotation_dialog,
                                         text="Confirmar Rotação",
                                         command=lambda: self.handle_on_click_confirm_transformation(rotation_dialog))

        rotation_button_done.pack()

    def handle_on_slider_rotation_slide(self, value):
        self.temporary_geometry_object_list = []
        for geometry_object in self.geometry_objects_list:
            rotated_object = GraphicAlgorithms.get_rotated_geometry_object(geometry_object, int(value))
            self.temporary_geometry_object_list.append(rotated_object)
        self.canvas.delete("all")
        self.render_geometry_objects_on_screen(self.temporary_geometry_object_list)

    def handle_on_click_confirm_transformation(self, scaling_dialog):
        scaling_dialog.destroy()
        self.dim = None
        self.render_geometry_objects_list_on_screen_and_overwrite_old_list(list(self.temporary_geometry_object_list))

    def handle_on_slider_scaling_slide(self, value, dim):
        self.valid_temporary_geometry_object_list(dim)
        for i in range(0, len(self.geometry_objects_list)):
            geometry_object = self.geometry_objects_list[i]
            scaled_geometry_object = GraphicAlgorithms.get_scaled_object(geometry_object, float(value), dim)
            self.temporary_geometry_object_list[i] = scaled_geometry_object
        self.canvas.delete("all")
        self.render_geometry_objects_on_screen(self.temporary_geometry_object_list)

    def valid_temporary_geometry_object_list(self, dim):
        if self.dim is None:
            self.dim = dim
        elif self.dim != dim:
            self.dim = dim
            if len(self.geometry_objects_list) == len(self.temporary_geometry_object_list):
                self.geometry_objects_list = list(self.temporary_geometry_object_list)
        if len(self.temporary_geometry_object_list) != len(self.geometry_objects_list):
            self.temporary_geometry_object_list = [0 for _ in range(0, len(self.geometry_objects_list))]

    def handle_on_click_scaling_button(self):
        if self.command != Command.NONE:
            messagebox.showerror(title="Error", message="Desmarque todos os botoes para utilizar este comando")
            return
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
                                      command=lambda: self.handle_on_click_confirm_transformation(scaling_dialog))

        scale_button_done.pack()

    def handle_on_click_translation_button(self):
        if self.command != Command.NONE:
            messagebox.showerror(title="Error", message="Desmarque todos os botoes para utilizar este comando")
            return
        translation_dialog = tk.Toplevel(self.window)
        translation_dialog.title("Escala")
        translation_dialog.geometry("200x200")
        tk.Label(translation_dialog,
                 text="Mova os sliders para transladar").pack()
        tk.Label(translation_dialog, text="Translação em X").pack()
        translate_x_slider = tk.Scale(translation_dialog,
                                      from_=-200,
                                      to=200,
                                      orient=tk.HORIZONTAL,
                                      length="200",
                                      command=lambda value: self.handle_on_slider_translation_slide(value, "x"))
        translate_x_slider.set(1)
        translate_x_slider.pack()
        tk.Label(translation_dialog, text="Translação em Y").pack()
        translate_y_slider = tk.Scale(translation_dialog,
                                      from_=-200,
                                      to=200,
                                      orient=tk.HORIZONTAL,
                                      length="200",
                                      command=lambda value: self.handle_on_slider_translation_slide(value, "y"))
        translate_y_slider.set(1)
        translate_y_slider.pack()
        scale_button_done = tk.Button(translation_dialog,
                                      text="Confirmar Translação",
                                      command=lambda: self.handle_on_click_confirm_transformation(translation_dialog))

        scale_button_done.pack()

    def handle_on_slider_translation_slide(self, value, dim):
        self.valid_temporary_geometry_object_list(dim)
        for i in range(0, len(self.geometry_objects_list)):
            geometry_object = self.geometry_objects_list[i]
            translated_geometry_object = GraphicAlgorithms.get_translated_geometry_object(geometry_object, int(value),
                                                                                          dim)
            self.temporary_geometry_object_list[i] = translated_geometry_object
        self.canvas.delete("all")
        self.render_geometry_objects_on_screen(self.temporary_geometry_object_list)

    def translate_geometry_objects(self, x, y):
        new_geometry_object_list = []
        for geometry_object in self.geometry_objects_list:
            new_geometry_object_list.append(GraphicAlgorithms.get_translated_geometry_object(geometry_object, x, y))
        self.render_geometry_objects_list_on_screen_and_overwrite_old_list(new_geometry_object_list)

    def render_geometry_objects_list_on_screen_and_overwrite_old_list(self, new_geometry_object_list):
        self.clean_screen()
        self.geometry_objects_list = new_geometry_object_list
        self.render_geometry_objects_on_screen(self.geometry_objects_list)

    def handle_on_click_menu_button(self, algorithm):
        self.command = algorithm
        self.clean_click_points()

    def clean_screen(self):
        self.canvas.delete("all")
        self.geometry_objects_list.clear()
        self.temporary_geometry_object_list.clear()

    def render_geometry_objects_on_screen(self, geometry_objects_list):
        for geometryObject in geometry_objects_list:
            if geometryObject.type == GeometryType.ddd_Line:
                self.ga.draw_dda_line(geometryObject.point1, geometryObject.point2)
            elif geometryObject.type == GeometryType.bresenham_Line:
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
        self.canvas.bind('<B1-Motion>', lambda event: self.handle_on_motion_screen(Point(event.x, event.y)))
        self.canvas.bind('<ButtonRelease-1>',
                         lambda event: self.handle_on_click_released_screen(Point(event.x, event.y)))
        self.canvas.bind('<Button-1>', lambda event: self.handle_on_click_screen(Point(event.x, event.y)))

    def handle_on_click_screen(self, point):
        if self.command == Command.COHEN_SUTHERLAND_CLIP or self.command == Command.LIANG_BARSKY_CLIP or self.command == Command.BRESENHAM_CIRCLE:
            if self.clip_first_point is None:
                self.firstPoint = point
                self.clip_first_point = point

    def handle_on_motion_screen(self, point):
        if self.command == Command.COHEN_SUTHERLAND_CLIP or self.command == Command.LIANG_BARSKY_CLIP:
            self.clip_second_point = point
            self.canvas.delete("all")
            point1, point2, point3, point4 = self.get_preview_clipped_area_limits()
            try:
                self.draw_rect(point1, point2, point3, point4)
            except:
                pass
            self.render_geometry_objects_on_screen(self.geometry_objects_list)
        if self.command == Command.BRESENHAM_CIRCLE:
            self.clip_second_point = point
            self.canvas.delete("all")
            radius = GraphicAlgorithms.compute_distance_between_two_points(self.clip_first_point, self.clip_second_point)
            self.ga.draw_bresenham_circle(self.clip_first_point, radius)
            self.render_geometry_objects_on_screen(self.geometry_objects_list)

    def draw_rect(self, point1, point2, point3, point4):
        self.ga.draw_dda_line(point1, point2)
        self.ga.draw_dda_line(point2, point3)
        self.ga.draw_dda_line(point3, point4)
        self.ga.draw_dda_line(point4, point1)

    def get_preview_clipped_area_limits(self):
        x_min = self.clip_first_point.x if self.clip_first_point.x < self.clip_second_point.x else self.clip_second_point.x
        y_min = self.clip_first_point.y if self.clip_first_point.y < self.clip_second_point.y else self.clip_second_point.y
        x_max = self.clip_first_point.x if self.clip_first_point.x > self.clip_second_point.x else self.clip_second_point.x
        y_max = self.clip_first_point.y if self.clip_first_point.y > self.clip_second_point.y else self.clip_second_point.y
        x_min = round(x_min)
        x_max = round(x_max)
        y_min = round(y_min)
        y_max = round(y_max)
        point1 = Point(x_min, y_max)
        point2 = Point(x_max, y_max)
        point3 = Point(x_max, y_min)
        point4 = Point(x_min, y_min)
        return point1, point2, point3, point4

    def handle_on_click_released_screen(self, point):
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
            if geometry_object.type != GeometryType.bresenham_Circle:
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
        bresenham_circle = GeometryObject(GeometryType.bresenham_Circle, self.firstPoint, radius=radius)
        self.geometry_objects_list.append(bresenham_circle)
        self.ga.draw_bresenham_circle(self.firstPoint, radius)

    def handle_click_bresenham_line(self):
        bresenham_line = GeometryObject(GeometryType.bresenham_Line, self.firstPoint, self.secondPoint)
        self.geometry_objects_list.append(bresenham_line)
        self.ga.draw_bresenham_line(self.firstPoint, self.secondPoint)

    def handle_click_dda_line(self):
        dda_line = GeometryObject(GeometryType.ddd_Line, self.firstPoint, self.secondPoint)
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
        self.clip_first_point = self.clip_second_point = None


def main():
    mg = MainGui()


if __name__ == '__main__':
    main()
