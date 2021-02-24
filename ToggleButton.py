import tkinter as tk

from Command import Command
from Metrics import Metrics


class ToggleButton:

    def __init__(self, master, text, command, algorithm, cleanButtons):
        self.master = master
        self.isPressed = False
        self.text = text
        self.command = command
        self.algorithm = algorithm
        self.cleanButtons = cleanButtons
        self.configureView()

    def configureView(self):
        self.btn = tk.Button(self.master,
                             text=self.text,
                             width=Metrics.buttonSize,
                             relief="raised",
                             command=self.toggle,
                             padx=Metrics.paddingMenuButtonsX,
                             pady=Metrics.paddingMenuButtonsY)
        self.btn.pack(side="left")

    def toggle(self):
        if self.btn.config('relief')[-1] == 'sunken':
            self.cleanButtons()
            self.btn.config(relief="raise")
            self.command(Command.NONE)
        else:
            self.cleanButtons()
            self.btn.config(relief="sunken")
            self.command(self.algorithm)
