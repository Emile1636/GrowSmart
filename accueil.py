# accueil.py : Vue d'ensemble de l'application
import customtkinter as ctk

class Accueil(ctk.CTkFrame):
    def __init__(self, master, main_frame, formulaire):
        super().__init__(master)
        self.main_frame = main_frame
        self.formulaire = formulaire
        self.utilisateur = None  # Stocker l'utilisateur connecté

    def afficher_accueil(self, utilisateur):
        self.utilisateur = utilisateur
        self.setup_colors()

        # Titre principal
        self.label_titre = ctk.CTkLabel(self.main_frame, text=f"Bienvenue {self.utilisateur}", font=("Helvetica", 40, "bold"), text_color=self.title_color_Grow)
        self.label_titre.grid(row=0, column=0, columnspan=2, pady=(20, 600)) # À changer l'espacement

        # Bouton de déconnexion
        self.button_deconnexion = ctk.CTkButton(self.main_frame, text="Se déconnecter", command=lambda:[self.masquer_accueil(), self.formulaire.afficher_formulaire()], fg_color=self.button_register_color, hover_color=self.button_register_color_hover, text_color=self.button_text_color, width=150, height=40, corner_radius=15, font=("Arial", 16, "bold"))
        self.button_deconnexion.grid(row=3, column=0, columnspan=2, pady=(10, 10))

        # Affichage des données des plantes
        self.afficher_donnees_plantes()

        ...

    def afficher_donnees_plantes(self):
        ...

    def masquer_accueil(self):
        self.label_titre.grid_remove()
        self.button_deconnexion.grid_remove()

    def setup_colors(self): # À modifier/ajuster, ce sont les couleurs du formulaire.
        # Couleurs (accès facile pour changer)
        # --- Texte
        self.background_color = "#F0F0F0"
        self.title_color_Grow = "#063831"
        self.title_color_Smart = "#028A0F"
        self.subtitle_color = "#4D4D4D"
        self.placeholder_text_color = "#ffffff"
        self.consigne = "#F14156"
        # --- Boutons
        self.button_register_color = "#355E3B"
        self.button_register_color_hover = "#294a2e"
        self.button_connect_color = "#028A0F"
        self.button_connect_color_hover = "#01750c"
        self.button_text_color = "#FFFFFF"
        # Config
        self.main_frame.configure(fg_color=self.background_color)
