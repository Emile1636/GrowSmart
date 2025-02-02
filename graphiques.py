#graphiques
import tkinter as tk
from customtkinter import CTkFrame
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from accueil import Accueil

class Graphiques():
    def __init__(self, master=None, series1=None, series2=None):
        super().__init__(master)
        self.master = master
        self.series1 = series1
        self.series2 = series2
        self.create_widgets()

    def bouton(self):
        self.grid(row=0, column=0, padx=20, pady=20, sticky="nsew") # Grille
        
        self.button = CTkFrame.CTkButton(self, text="Voir les graphiques", command=self.create_graphics) # Bouton
        self.button.grid(row=0, column=0, pady=(20,10))

        self.label = CTkFrame.CTkLabel(self, text="CTkLabel", fg_color="transparent")# Label
        self.label.grid(row=1, column=0, pady=(10,10))


    def create_graphics(self):
        # Créer le graphique
        plt.figure(figsize=(5, 4))
        plt.plot(self.series1, self.series2, label='Le carrée de la série 1', color='b')
        plt.title('Graphique des séries')
        plt.xlabel('Série 1')
        plt.ylabel('Série 2')
        plt.legend()
        plt.grid()
        
        # Intégrer le graphique dans tkinter
        self.canvas = FigureCanvasTkAgg(plt.gcf(), master=self)
        self.canvas.draw()
        self.canvas.get_tk_widget().grid(row=2, column=0, pady=(10,10))


