# formulaire.py
import customtkinter as ctk
import json
from disciplines_scientifiques.RSA import RSA

class Formulaire:
    def __init__(self, master, main_frame, app):
        self.master = master
        self.main_frame = main_frame
        self.app = app # Référence à l'instance de Application
        self.screen_width = self.master.winfo_screenwidth()
        self.screen_height = self.master.winfo_screenheight()
    
    def set_accueil(self, accueil):
        self.accueil = accueil

    def afficher_formulaire(self):
        self.setup_colors() # Setup les couleurs
        # Titre: GrowSmart
        self.label_grow = ctk.CTkLabel(self.main_frame, text="Grow", font=("Helvetica", 180, "bold"), text_color=self.title_color_Grow)
        self.label_grow.grid(row=0, column=0, padx=(20, 0), pady=(50, 0), sticky="e")
        self.label_smart = ctk.CTkLabel(self.main_frame, text="Smart", font=("Helvetica", 180, "bold"), text_color=self.title_color_Smart)
        self.label_smart.grid(row=0, column=1, padx=(0, 20), pady=(50, 0), sticky="w")

        # Sous-titres
        self.label_subtitle = ctk.CTkLabel(self.main_frame, text="Surveillez, gérez, et faites fleurir ", font=("Aptos", 32, "italic"), text_color=self.subtitle_color)
        self.label_subtitle.grid(row=1, column=0, columnspan=2, pady=(10, 50))

        # Champs: Nom d'utilisateur et mot de passe
        self.entry_username = ctk.CTkEntry(self.main_frame, placeholder_text="Nom d'utilisateur", font=("Helvetica", 18), width=350, height=50, corner_radius=15, fg_color=self.placeholder_text_color, text_color="#000000", border_width=1, border_color="#999999")
        self.entry_username.grid(row=2, column=0, columnspan=2, pady=(10, 10))
        self.entry_password = ctk.CTkEntry(self.main_frame, placeholder_text="Mot de passe", show="*", font=("Helvetica", 18), width=350, height=50, corner_radius=15, fg_color=self.placeholder_text_color, text_color="#000000", border_width=1, border_color="#999999")
        self.entry_password.grid(row=3, column=0, columnspan=2, pady=(10, 30)) #Problème lorsque mots de passe ou utilisateur incorrect: impossible d'écrire une nouvelle réponse

        # Boutons
        self.button_connect = ctk.CTkButton(self.main_frame, text="Se connecter", command=self.connexion, fg_color=self.button_connect_color, hover_color=self.button_connect_color_hover, text_color=self.button_text_color, width=140, height=40, corner_radius=20, font=("Arial", 16, "bold"))
        self.button_connect.grid(row=4, column=0, columnspan=2, pady=(10, 10))
        self.button_register = ctk.CTkButton(self.main_frame, text="S'inscrire", command=self.inscription, fg_color=self.button_register_color, hover_color=self.button_register_color_hover, text_color=self.button_text_color, width=140, height=40, corner_radius=20, font=("Arial", 16, "bold"))
        self.button_register.grid(row=6, column=0, columnspan=2, pady=(10, 10))

        # Diviser les boutons
        self.divider_line = ctk.CTkLabel(self.main_frame, text="————————  OU  ————————", font=("Arial", 16, "bold"), text_color=self.subtitle_color)
        self.divider_line.grid(row=5, column=0, columnspan=2, pady=(10, 10))

    def connexion(self):
        self.username = self.entry_username.get()
        self.password = self.entry_password.get()

        with open("users.json", "r") as f: # Récuéperer les identifiants des utilisateurs
            self.liste_utilisateurs = json.load(f)

        if not self.username:
            self.entry_username.configure(placeholder_text="Veuillez remplir ce champs", placeholder_text_color=self.consigne, font=("Helvetica", 18))
            return 
        
        if not self.password:
            self.entry_password.configure(placeholder_text="Veuillez remplir ce champs", placeholder_text_color=self.consigne, font=("Helvetica", 18))
            return

        if self.username not in self.liste_utilisateurs:
            self.entry_username.delete(0, "end")
            self.entry_username.configure(placeholder_text="Nom d'utilisateur introuvable", placeholder_text_color=self.consigne, font=("Helvetica", 18))
            return
        
        
        self.RSA_password = self.liste_utilisateurs[self.username]["password"]
        self.password_chiffrer=RSA.vérifier_mot(self.username,self.password) #Transforme self.password en RSA

        if self.RSA_password == self.password_chiffrer: #Comparaison des deux code RSA
            self.afficher_connexion_reussi()
        else:
            self.entry_password.delete(0, "end")
            self.entry_password.configure(placeholder_text="Mot de passe erroné", placeholder_text_color=self.consigne, font=("Helvetica", 18))

    def inscription(self):
        self.masquer_formulaire()
        self.afficher_formulaire_inscription()

    def afficher_formulaire_inscription(self):
        self.label_register_title = ctk.CTkLabel(self.main_frame, text="Créer un compte", font=("Helvetica", 32, "bold"), text_color="#4D4D4D")
        self.label_register_title.grid(row=0, column=0, columnspan=2, pady=(50, 20))

        self.entry_new_username = ctk.CTkEntry(self.main_frame, placeholder_text="Nom d'utilisateur", font=("Helvetica", 18), width=350, height=50, corner_radius=15, fg_color="#ffffff", text_color="#000000", border_width=1, border_color="#999999")
        self.entry_new_username.grid(row=1, column=0, columnspan=2, pady=(10, 10))

        self.entry_new_password = ctk.CTkEntry(self.main_frame, placeholder_text="Mot de passe", show="*", font=("Helvetica", 18), width=350, height=50, corner_radius=15, fg_color="#ffffff", text_color="#000000", border_width=1, border_color="#999999")
        self.entry_new_password.grid(row=2, column=0, columnspan=2, pady=(10, 10))

        self.entry_confirm_password = ctk.CTkEntry(self.main_frame, placeholder_text="Confirmer le mot de passe", show="*", font=("Helvetica", 18), width=350, height=50, corner_radius=15, fg_color="#ffffff", text_color="#000000", border_width=1, border_color="#999999")
        self.entry_confirm_password.grid(row=3, column=0, columnspan=2, pady=(10, 30))

        self.button_register_submit = ctk.CTkButton(self.main_frame, text="S'inscrire", command=self.submit_registration, fg_color="#355E3B", hover_color="#294a2e", text_color="#FFFFFF", width=140, height=40, corner_radius=20, font=("Arial", 16, "bold"))
        self.button_register_submit.grid(row=4, column=0, columnspan=2, pady=(10, 10))

        self.button_back = ctk.CTkButton(self.main_frame, text="Retour", command=lambda:[self.masquer_formulaire_inscription(), self.afficher_formulaire()], fg_color="#CCCCCC", hover_color="#AAAAAA", text_color="#000000", width=140, height=40, corner_radius=20, font=("Arial", 16, "bold"))
        self.button_back.grid(row=5, column=0, columnspan=2, pady=(10, 10))

    def submit_registration(self):
        self.new_username = self.entry_new_username.get()
        self.new_password = self.entry_new_password.get()
        self.confirm_password = self.entry_confirm_password.get()

        with open("users.json", "r") as f: # Récuéperer les identifiants des utilisateurs
            self.liste_utilisateurs = json.load(f)

        # return partout, car ca ne sert a rien d'aller plus loins si les conditions ne sont pas respecté
        # cela explique la foulé de return pour toutes les conditions suivantes 

        if self.new_username in self.liste_utilisateurs:
            self.entry_new_username.delete(0, "end")
            self.entry_new_username.configure(placeholder_text="Nom d'utilisateur déjà utilisé", placeholder_text_color=self.consigne, font=("Helvetica", 18))
            return 
        
        if not self.new_username:
            self.entry_new_username.configure(placeholder_text="Veuillez remplir ce champs", placeholder_text_color=self.consigne, font=("Helvetica", 18))
            return 
        
        if not self.new_password:
            self.entry_new_password.configure(placeholder_text="Veuillez remplir ce champs", placeholder_text_color=self.consigne, font=("Helvetica", 18))
            return
        
        if not self.confirm_password:
            self.entry_confirm_password.configure(placeholder_text="Veuillez remplir ce champs", placeholder_text_color=self.consigne, font=("Helvetica", 18))
            return 
                   
        if self.new_password != self.confirm_password:
            self.entry_new_password.delete(0, "end")
            self.entry_new_password.configure(placeholder_text="Mots de passes non identiques", placeholder_text_color=self.consigne, font=("Helvetica", 18))
            self.entry_confirm_password.delete(0, "end")
            return
        
        if len(self.new_username) < 4:
            self.entry_new_username.delete(0, "end")
            self.entry_new_username.configure(placeholder_text="Nom d'utilisateur trop court", placeholder_text_color=self.consigne, font=("Helvetica", 18))
            return
        
        if len(self.new_password) < 5:
            self.entry_new_password.delete(0, "end")
            self.entry_new_password.configure(placeholder_text="Mot de passe trop court", placeholder_text_color=self.consigne, font=("Helvetica", 18))
            self.entry_confirm_password.delete(0, "end")
            return
        
        if self.new_username == self.new_password:
            self.entry_new_password.delete(0, "end")
            self.entry_new_password.configure(placeholder_text="Doit être différent du nom d'utilisateur", placeholder_text_color=self.consigne, font=("Helvetica", 18))
            self.entry_confirm_password.delete(0, "end")
            return           

       
        
        # Important d'avoir mis des return après les vérifiactions précédentes sinon le code suivant s'execute quand même

        RSA.noter_nouv_élém(self.new_username, self.new_password)   #note le nouveau mot de passe en RSA

        # self.liste_utilisateurs[self.new_username] = {"password": self.new_password } # Mot de passe sans RSA
        # with open("users.json", "w") as f:
        #     json.dump(self.liste_utilisateurs, f, indent=4)
        
        # Fin
        self.masquer_formulaire_inscription()
        self.afficher_formulaire()

    def afficher_connexion_reussi(self):
            self.masquer_formulaire()
            self.label_connexion_reussi = ctk.CTkLabel(self.main_frame, text=" Connexion réussie ",font=("Aptos", 40, "bold", "italic"), text_color="#4D4D4D")
            self.label_connexion_reussi.grid(row=0, column=0, columnspan=2, pady=(0, 50))
            self.master.after(1000, lambda: [self.label_connexion_reussi.grid_remove(), self.accueil.afficher_accueil(self.username)])

    def masquer_formulaire(self):
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
        self.entry_new_password.grid_remove()
        self.entry_confirm_password.grid_remove()
        self.button_register_submit.grid_remove()
        self.button_back.grid_remove()

    def setup_colors(self):
        # Couleurs (accès facile pour changer)
        # --- Texte
        self.background_color = "#fffcfc" # Nouvelle couleur de fond plutot que #F0F0F0

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
