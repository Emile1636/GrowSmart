# interface.py
import tkinter as tk
from customtkinter import CTkFrame
from formulaire import Formulaire
from accueil import Accueil

class Interface(CTkFrame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.setup()

    def setup(self):
        # Initialisation et configuration du frame
        color_back = "#fffcfc"
        self.configure(fg_color=color_back)
        self.main_frame = CTkFrame(self, fg_color=color_back)
        self.main_frame.grid(sticky="nsew")
        self.main_frame.place(relx=0.5, rely=0.5, anchor="center")

        # Création des "pages" en évitant une initialisation circulaire
        self.formulaire = Formulaire(self.master, self.main_frame, self)
        self.accueil = Accueil(self.master, self.main_frame, self.formulaire)
        self.formulaire.set_accueil(self.accueil)
        
        self.formulaire.afficher_formulaire() # Lancer l'accueil par défaut
