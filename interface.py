# interface.py
import tkinter as tk
from customtkinter import CTkFrame
from formulaire import Formulaire

class Interface(CTkFrame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.setup()

    def setup(self):
        color_back = "#F0F0F0"
        self.configure(fg_color=color_back)
        self.main_frame = CTkFrame(self, fg_color=color_back)
        self.main_frame.grid(sticky="nsew")
        self.main_frame.place(relx=0.5, rely=0.5, anchor="center")

        self.formulaire = Formulaire(self.master, self.main_frame, self)
        self.formulaire.afficher_formulaire()