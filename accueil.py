# accueil.py : Vue d'ensemble de l'application
import customtkinter as ctk
import json
import os
from PIL import Image
from plante import Plante

class Accueil(ctk.CTkFrame):
    def __init__(self, master, main_frame, formulaire):
        super().__init__(master)
        self.main_frame = main_frame
        self.formulaire = formulaire
        self.page_setup_plante = Plante(master, main_frame, self)
        self.screen_l = master.winfo_screenwidth()
        self.screen_h = master.winfo_screenheight()
        self.liste_utilisateurs = {}
        self.utilisateur = ""
        self.nb_plante = 0
        self.plantes = {}

    def afficher_accueil(self, utilisateur):
        self.load_user(utilisateur)
        self.setup_colors()
        self.cree_labels()
        # Afficher les éléments de l'accueil
        if self.nb_plante == 0:
            self.afficher_entete_initale()
        else:
            self.afficher_entete_plantes()

    def afficher_entete_initale(self):
        # Titre principal 
        self.label_bienvenue.grid(row=0, column=0, padx=(0, (self.screen_l-(275+len(self.utilisateur)*15))), pady=(self.screen_l/14.7, 0), sticky="w")
        # Bouton de déconnexion
        self.bouton_deconnexion.grid(row=0, column=0, padx=(0, 0), pady=(self.screen_l/14.7, 0), sticky="e") # /36
        # Titre "Votre Jardin"
        self.label_titre.grid(row=1, column=0, padx=(0, 0), pady=(0, self.screen_h/3))
        # Instruction pour ajouter une plante
        self.label_instruction.grid(row=2, column=0, padx=(0, 0), pady=(0, self.screen_h/1.9))
       
    def afficher_entete_plantes(self):
        # Repositionnement des éléments
        self.label_bienvenue.grid(row=0, column=0, padx=(0, (self.screen_l-(275+len(self.utilisateur)*15))), pady=(0, 0), sticky="w")
        # Bouton de déconnexion
        self.bouton_deconnexion.grid(row=0, column=0, padx=(0, 0), pady=(0, 0), sticky="e")
        # Titre "Votre Jardin"
        self.label_titre.grid(row=1, column=0, padx=(0, 0), pady=(0, self.screen_l/30))
        
        # Instruction pour ajouter une plante (seulement si moins de 5 plantes)
        if self.nb_plante < 5:
            self.label_instruction.configure(text="Ajoutez une nouvelle plante", font=("Helvetica", 24, "bold"))
            self.label_instruction.bind("<Enter>", lambda event: self.label_instruction.configure(text="Ajoutez une nouvelle plante",font=("Helvetica", 24, "bold", "underline")))  # Changement de texte au survol
            self.label_instruction.bind("<Leave>", lambda event: self.label_instruction.configure(text="Ajoutez une nouvelle plante",font=("Helvetica", 24, "bold")))  # Rétablir le texte
            self.label_instruction.grid(row=3, column=0, padx=(0, 0), pady=(0, self.screen_l/35)) 
        else:
            # Cacher le label instruction quand on a atteint 5 plantes
            self.label_instruction.grid_remove()
            self.tempo.grid(row=3, column=0, padx=(0, 0), pady=(0, self.screen_l/35))
            
        self.afficher_plante()
    
    def afficher_plante(self):
        if self.nb_plante < 1: return

        # Créer un conteneur pour les plantes
        self.plants_container = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.plants_container.grid(row=2, column=0, pady=10)
        
        # Configurer le conteneur pour centrer son contenu
        for i in range(min(5, self.nb_plante)):
            self.plants_container.grid_columnconfigure(i, weight=1)

        # Récupérer les informations des plantes enregistrées
        plantes_data = self.liste_utilisateurs.get(self.utilisateur, {}).get("plantes", {})
        
        # Afficher jusqu'à 5 plantes
        for i in range(min(5, self.nb_plante)):
            plante_key = f"plante {i+1}"
            plante_nom = plantes_data.get(plante_key, {}).get("nom", "Plante inconnue")
            
            # Créer un cadre pour afficher les informations de la plante
            plante_frame = ctk.CTkFrame(self.plants_container, corner_radius=20, fg_color="#E8F5E9")
            plante_frame.grid(row=0, column=i, pady=10, padx=(10 if i > 0 else 0, 10))
            
            # Ajouter l'image de la plante avec redimensionnement
            plante_image = ctk.CTkImage(light_image=Image.open(f'images/plante {i+1}.png'), size=(self.screen_l/8, self.screen_l/11))
            label_image = ctk.CTkLabel(plante_frame, image=plante_image, text="")
            label_image.grid(row=0, column=0, pady=20, padx=(10, 10))
            
            # Afficher le nom de la plante
            plante_nom_label = ctk.CTkLabel(plante_frame, text=plante_nom, font=("Helvetica", 24, "bold"), text_color=self.subtitle_color)
            plante_nom_label.grid(row=1, column=0, pady=(10, self.screen_h/3))
            
            # Bouton "Voir plus" pour afficher les détails
            bouton_voir_plus = ctk.CTkButton(plante_frame, text="Voir plus", command=lambda i=i+1: [self.masquer_accueil(), self.page_setup_plante.afficher_plante(i)], font=("Helvetica", 18, "bold"), corner_radius=15, fg_color="#4CAF50", hover_color="#3e8e41", text_color=self.button_text_color)
            bouton_voir_plus.grid(row=2, column=0, pady=(0, self.screen_h/30)) 
            
            # Stocker les références comme attributs de classe 
            setattr(self, f"plante_{i+1}_frame", plante_frame)
            setattr(self, f"plante_image{i+1}", plante_image)
            setattr(self, f"label_image{i+1}", label_image)
            setattr(self, f"plante_{i+1}_nom", plante_nom_label)
            setattr(self, f"bouton_voir_plus_{i+1}", bouton_voir_plus)

    def cree_labels(self):
        # Configure la colonne pour étirer correctement les éléments
        self.main_frame.grid_columnconfigure(0, weight=1)
        
        # Titre principal (non cliquable)
        self.label_bienvenue = ctk.CTkLabel(self.main_frame, text=f"Bienvenue {self.utilisateur}", font=("Helvetica", 35, "bold"), text_color=self.subtitle_color)
        
        # Bouton de déconnexion (conçu comme un label cliquable, similaire au label bienvenue original)
        self.bouton_deconnexion = ctk.CTkLabel(self.main_frame, text="Se déconnecter", font=("Helvetica", 35, "bold"), text_color=self.subtitle_color)
        self.bouton_deconnexion.bind("<Button-1>", lambda event: self.deconnecter())  # Ajout du clic
        self.bouton_deconnexion.bind("<Enter>", lambda event: self.bouton_deconnexion.configure(font=("Helvetica", 35, "bold", "underline")))  # Soulignement au survol
        self.bouton_deconnexion.bind("<Leave>", lambda event: self.bouton_deconnexion.configure(font=("Helvetica", 35, "bold")))  # Retour à normal
        
        # Titre "Votre Jardin"
        self.label_titre = ctk.CTkLabel(self.main_frame, text="Votre Jardin", font=("Helvetica", 40, "bold"), text_color=self.subtitle_color)
        # Instruction pour ajouter une plante
        self.label_instruction = ctk.CTkLabel(self.main_frame, text="Ajoutez une plante pour commencer", font=("Helvetica", 24, "bold"), text_color=self.subtitle_color)
        self.label_instruction.bind("<Button-1>", lambda event: self.cree_plante())  # Ajout du clic
        self.label_instruction.bind("<Enter>", lambda event: self.label_instruction.configure(font=("Helvetica", 24, "bold", "underline")))  # Changement de texte au survol
        self.label_instruction.bind("<Leave>", lambda event: self.label_instruction.configure(font=("Helvetica", 24, "bold")))  # Rétablir le texte
        self.tempo = ctk.CTkLabel(self.main_frame, text="", font=("Helvetica", 24, "bold"))

    def load_user(self, utilisateur):
        # Vérifier si le fichier existe, sinon le créer
        if not os.path.exists("users.json"):
            with open("users.json", "w") as file:
                json.dump({}, file)
                
        with open("users.json", "r") as file:
            self.liste_utilisateurs = json.load(file)

        self.utilisateur = utilisateur  # Stocker l'utilisateur connecté
        
        # Vérifier si l'utilisateur existe dans le fichier
        if self.utilisateur not in self.liste_utilisateurs:
            self.liste_utilisateurs[self.utilisateur] = {"nb_plante": 0, "plantes": {}}
            with open("users.json", "w") as f:
                json.dump(self.liste_utilisateurs, f, indent=4)
        
        self.nb_plante = self.liste_utilisateurs[self.utilisateur].get("nb_plante", 0)
        if self.nb_plante > 0:
            self.plantes = self.liste_utilisateurs[self.utilisateur].get("plantes", {})

    def cree_plante(self):
        # Vérifier si on n'a pas déjà 5 plantes
        if self.nb_plante >= 5:
            return  # Ne rien faire si on a déjà 5 plantes
            
        # Ajouter la clé "plantes" sans écraser les données existantes
        self.liste_utilisateurs[self.utilisateur].setdefault("plantes", {})
        self.liste_utilisateurs[self.utilisateur]["plantes"][f"plante {self.nb_plante+1}"] = {
            "nom": "Inconnu",
            "capteur": "",
            "type": "" ,
            "date_plantation":["","",""],
            "superficie": ""
        }
        # Incrémenter le nombre de plantes
        self.nb_plante += 1
        self.liste_utilisateurs[self.utilisateur]["nb_plante"] = self.nb_plante
        # Enregistrer les modifications
        with open("users.json", "w") as f:
            json.dump(self.liste_utilisateurs, f, indent=4)

        # Effacer l'affichage actuel et mettre à jour
        self.masquer_accueil()
        self.afficher_accueil(self.utilisateur)

    def deconnecter(self):
        self.masquer_accueil()
        self.formulaire.afficher_formulaire()

    def masquer_accueil(self):
        # Supprimer les éléments d'interface de manière plus robuste
        for widget in [self.label_bienvenue, self.bouton_deconnexion, self.label_titre, self.label_instruction, self.tempo]:
            try:
                widget.grid_remove()
            except AttributeError:
                pass
        # Supprimer le conteneur de plantes s'il existe
        try:
            self.plants_container.grid_remove()
        except AttributeError:
            pass
        # Supprimer chaque frame de plante individuellement
        for i in range(1, 6):
            try:
                frame = getattr(self, f"plante_{i}_frame")
                frame.grid_remove()
            except AttributeError:
                pass

    def setup_colors(self):
        self.background_color = "#fffcfc"
        self.subtitle_color = "#4D4D4D"
        self.consigne = "#F14156"
        self.button_text_color = "#FFFFFF"
        self.main_frame.configure(fg_color=self.background_color)