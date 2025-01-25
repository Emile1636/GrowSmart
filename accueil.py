# accueil.py
import customtkinter as ctk

class Accueil:
    def __init__(self, master, main_frame, app):
        self.master = master
        self.main_frame = main_frame
        self.nom_user = ""
        self.app = app
        self.screen_width = self.master.winfo_screenwidth()
        self.screen_height = self.master.winfo_screenheight()

    def set_formulaire(self, formulaire):
        self.formulaire = formulaire

    def set_nom_user(self, pseudo):
        self.nom_user = pseudo

    def get_nom_user(self):
        if self.nom_user == "":
            return "Inconnu"
        else:
            return self.nom_user

    def afficher_accueil(self):
        # Couleurs (accès facile pour changer)
        # --- Texte
        background_color = "#F0F0F0"
        title_color_Grow = "#063831"
        title_color_Smart = "#028A0F"
        subtitle_color = "#4D4D4D"
        placeholder_text_color = "#ffffff"
        # --- Boutons
        button_register_color = "#355E3B"
        button_register_color_hover = "#294a2e"
        button_connect_color = "#028A0F"
        button_connect_color_hover = "#01750c"
        button_text_color = "#FFFFFF"
        # Config
        self.main_frame.configure(fg_color=background_color)

        # Titre: GrowSmart
        self.label_grow = ctk.CTkLabel(
            self.main_frame, text="Grow", font=("Helvetica", 180, "bold"), text_color=title_color_Grow
        )
        self.label_grow.grid(row=0, column=0, padx=(20, 0), pady=(50, 0), sticky="e")

        self.label_smart = ctk.CTkLabel(
            self.main_frame, text="Smart", font=("Helvetica", 180, "bold"), text_color=title_color_Smart
        )
        self.label_smart.grid(row=0, column=1, padx=(0, 20), pady=(50, 0), sticky="w")

        # Sous-titres
        self.label_subtitle = ctk.CTkLabel(self.main_frame,
            text="Surveillez, gérez, et faites fleurir ",
            font=("Helvetica", 32, "italic"),
            text_color=subtitle_color,
        )
        self.label_subtitle.grid(row=1, column=0, columnspan=2, pady=(10, 50))

        # Champs: Nom d'utilisateur et mot de passe
        self.entry_username = ctk.CTkEntry(self.main_frame, 
            placeholder_text="Nom d'utilisateur", font=("Helvetica", 18), width=350, height=50, corner_radius=15, fg_color=placeholder_text_color, text_color="#000000", border_width=1, border_color="#000000"
        )
        self.entry_username.grid(row=2, column=0, columnspan=2, pady=(10, 10))

        self.entry_password = ctk.CTkEntry(self.main_frame, 
            placeholder_text="Mot de passe", show="*", font=("Helvetica", 18), width=350, height=50, corner_radius=15, fg_color=placeholder_text_color, text_color="#000000", border_width=1, border_color="#000000"
        )
        self.entry_password.grid(row=3, column=0, columnspan=2, pady=(10, 30))

        # Boutons
        self.button_connect = ctk.CTkButton(self.main_frame,
            text="Se connecter",
            command=self.connexion,
            fg_color=button_connect_color,
            hover_color=button_connect_color_hover,
            text_color=button_text_color,
            width=140, height=40, corner_radius=20,
            font=("Arial", 16, "bold")
        )
        self.button_connect.grid(row=4, column=0, columnspan=2, pady=(10, 10))

        # Diviser les boutons
        self.divider_line = ctk.CTkLabel(
            self.main_frame, text="————————  OU  ————————",
            font=("Arial", 16, "bold"),
            text_color=subtitle_color,
        )
        self.divider_line.grid(row=5, column=0, columnspan=2, pady=(10, 10))

        self.button_register = ctk.CTkButton(self.main_frame,
            text="S'inscrire",
            command=self.inscription,
            fg_color=button_register_color,
            hover_color=button_register_color_hover,
            text_color=button_text_color,
            width=140, height=40, corner_radius=20,
            font=("Arial", 16, "bold")
        )
        self.button_register.grid(row=6, column=0, columnspan=2, pady=(10, 10))

    def connexion(self):
        username = self.entry_username.get()
        password = self.entry_password.get()

        if username == "" or password == "":
            print("Veuillez remplir tous les champs.")
            # Vérification ...
        else:
            print(f"Connexion réussie pour l'utilisateur: {username}")
            # self.go_to_dashboard()  # exemple
            ...

    def inscription(self):
        self.masquer_accueil()
        self.afficher_formulaire_inscription()

    def afficher_formulaire_inscription(self):
        self.label_register_title = ctk.CTkLabel(
            self.main_frame, text="Créer un compte",
            font=("Helvetica", 32, "bold"), text_color="#4D4D4D"
        )
        self.label_register_title.grid(row=0, column=0, columnspan=2, pady=(50, 20))

        self.entry_new_username = ctk.CTkEntry(
            self.main_frame, placeholder_text="Nom d'utilisateur",
            font=("Helvetica", 18), width=350, height=50,
            corner_radius=15, fg_color="#ffffff", text_color="#000000",
            border_width=1, border_color="#000000"
        )
        self.entry_new_username.grid(row=1, column=0, columnspan=2, pady=(10, 10))

        self.entry_new_password = ctk.CTkEntry(
            self.main_frame, placeholder_text="Mot de passe", show="*",
            font=("Helvetica", 18), width=350, height=50,
            corner_radius=15, fg_color="#ffffff", text_color="#000000",
            border_width=1, border_color="#000000"
        )
        self.entry_new_password.grid(row=2, column=0, columnspan=2, pady=(10, 10))

        self.entry_confirm_password = ctk.CTkEntry(
            self.main_frame, placeholder_text="Confirmer le mot de passe", show="*",
            font=("Helvetica", 18), width=350, height=50,
            corner_radius=15, fg_color="#ffffff", text_color="#000000",
            border_width=1, border_color="#000000"
        )
        self.entry_confirm_password.grid(row=3, column=0, columnspan=2, pady=(10, 30))

        self.button_register_submit = ctk.CTkButton(
            self.main_frame, text="S'inscrire",
            command=self.submit_registration,
            fg_color="#355E3B", hover_color="#294a2e",
            text_color="#FFFFFF", width=140, height=40,
            corner_radius=20, font=("Arial", 16, "bold")
        )
        self.button_register_submit.grid(row=4, column=0, columnspan=2, pady=(10, 10))

        self.button_back = ctk.CTkButton(
            self.main_frame, text="Retour",
            command=lambda:[self.masquer_formulaire_inscription(), self.afficher_accueil()],
            fg_color="#CCCCCC", hover_color="#AAAAAA",
            text_color="#000000", width=140, height=40,
            corner_radius=20, font=("Arial", 16, "bold")
        )
        self.button_back.grid(row=5, column=0, columnspan=2, pady=(10, 10))

    def submit_registration(self):
        new_username = self.entry_new_username.get()
        new_password = self.entry_new_password.get()
        confirm_password = self.entry_confirm_password.get()

        if new_username == "" or new_password == "" or confirm_password == "":
            print("Veuillez remplir tous les champs.")
        elif new_password != confirm_password:
            print("Les mots de passe ne correspondent pas.")
        else:
            print(f"Inscription réussie pour l'utilisateur: {new_username}")
            self.masquer_formulaire_inscription()
            self.afficher_accueil()
            # Ajouter plusieurs choses (databse etc)
    
    def masquer_accueil(self):
        self.label_grow.grid_remove()
        self.label_smart.grid_remove()
        self.label_subtitle.grid_remove()
        self.entry_username.grid_remove()
        self.entry_password.grid_remove()
        self.button_connect.grid_remove()
        self.button_register.grid_remove()
        self.divider_line.grid_remove()

    def masquer_formulaire_inscription(self):
        self.label_register_title.grid_remove()
        self.entry_new_username.grid_remove()
        self.entry_confirm_password.grid_remove()
        self.button_register_submit.grid_remove()
        self.button_back.grid_remove()
