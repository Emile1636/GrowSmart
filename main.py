# main.py
import tkinter as tk
from customtkinter import CTk
from interface import Interface

class Application(CTk): # Class principale 
    def __init__(self):
        # Initialisation de la fenêtre principale
        super().__init__()
        self.title("GrowSmart")
        self.attributes('-fullscreen', True) #Émile
        # self.geometry(f"{self.winfo_screenwidth()}x{self.winfo_screenheight()}+{-100}")
    
        self.bar_menu()
        self.interface = Interface(self)
        self.interface.pack(fill=tk.BOTH, expand=True)

    def bar_menu(self):
        menu_bar = tk.Menu(self) # Creation de la bar de menu 
        self.config(menu=menu_bar)
        file_menu = tk.Menu(menu_bar, tearoff=0) # Creation de longlet 
        menu_bar.add_cascade(label="Option", menu=file_menu) # Ajout de longelt fichier
        file_menu.add_command(label="Quitter", command=self.quit) # Ajout de la commande quitter
        
    def quit_app(self):
        self.quit()

if __name__ == "__main__": # Vérification si ce fichier est exécuté en tant que programme principal
    app = Application() 
    app.protocol("WM_DELETE_WINDOW", app.quit()) # Permet deviter les problèmes lors de la fermeture
    app.mainloop()
