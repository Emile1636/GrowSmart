# plante.py : Vue détaillée d'une plante sélectionnée
import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
import json
import os
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from disciplines_scientifiques.energie import Energie
from disciplines_scientifiques.predictions import Predictions
from load_fichier_csv import load_data_from_gist
from disciplines_scientifiques.graph import Graph
from disciplines_scientifiques.derivee import Derivee

class Plante(ctk.CTkFrame):
    def __init__(self, master, main_frame, accueil):
        super().__init__(master)
        self.main_frame = main_frame
        self.accueil = accueil
        self.screen_l = master.winfo_screenwidth()
        self.screen_h = master.winfo_screenheight()
        self.setup_colors()
        self.plante_courante = None
        self.no_plante = None
        self.no_capteur = None
        self.liste_utilisateurs = {}
        self.utilisateur = ""
        self.liste_types_plantes = ["Conifère", "Feuillus", "Plante à fleurs", "Plante tropicale", "Cactus", "Fougère", "Herbe/Graminée", "Plante aquatique", "Légume", "Fruit", "Autre"]

    def afficher_plante(self, no_plante, utilisateur=None):
        # Si l'utilisateur est spécifié, l'utiliser, sinon prendre celui de l'accueil
        self.utilisateur = utilisateur if utilisateur else self.accueil.utilisateur
        self.no_plante = no_plante
        self.masquer_plante() # Nettoyer avant d'afficher
        
        # Charger les données utilisateur
        self.load_user_data()
        self.plante_courante = self.liste_utilisateurs.get(self.utilisateur, {}).get("plantes", {}).get(f"plante {no_plante}", {})
        
        # Vérifier si la plante est configurée
        if not self.plante_est_configuree():
            self.afficher_ecran_configuration()
        else:
            self.afficher_plante_configuree()
    
    def plante_est_configuree(self):
        # Vérifier si la plante a des informations "minimales" configurées
        # On considère qu'une plante est configurée si elle a au moins un nom autre que "Inconnu"
        return bool(self.plante_courante.get("nom") != "Inconnu")
    
    def load_user_data(self):
        # Vérifier si le fichier existe, sinon le créer
        if not os.path.exists("users.json"):
            with open("users.json", "w") as file:
                json.dump({}, file)
                
        with open("users.json", "r") as file:
            self.liste_utilisateurs = json.load(file)
    
    def masquer_plante(self):
        # Supprimer tous les widgets du main_frame (à voir si on aura des problèmes ou pas)
        for widget in self.main_frame.winfo_children():
            widget.grid_forget()
            
    def afficher_ecran_configuration(self):
        # Configurer la grille principale
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(0, weight=1)
        
        # Frame central pour la configuration
        self.config_frame = ctk.CTkFrame(self.main_frame, fg_color=self.background_color)
        self.config_frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        self.config_frame.grid_columnconfigure(0, weight=1)
        
        # Titre
        titre = ctk.CTkLabel(self.config_frame, text="Nouvelle Plante", font=("Helvetica", 36, "bold"), text_color=self.subtitle_color)
        titre.grid(row=0, column=0, pady=(20, 30))
        
        # Message d'information
        info = ctk.CTkLabel(self.config_frame, text="Cette plante n'est pas encore configurée", font=("Helvetica", 18), text_color=self.subtitle_color)
        info.grid(row=1, column=0, pady=(0, 30))
        
        # Bouton de configuration
        configurer_btn = ctk.CTkButton(self.config_frame, text="Configurer la plante", command=self.modifier_plante,font=("Helvetica", 20, "bold"), corner_radius=20, fg_color="#4CAF50", hover_color="#3e8e41", text_color=self.button_text_color,height=40, width=200)
        configurer_btn.grid(row=2, column=0, pady=30)
        
        # Bouton retour
        retour_btn = ctk.CTkButton(self.config_frame, text="← Retour", command=self.retour_accueil, font=("Helvetica", 18), corner_radius=15, fg_color="#AAAAAA", hover_color="#CCCCCC", text_color=self.button_text_color)
        retour_btn.grid(row=3, column=0, pady=20)
        
    def modifier_plante(self):
        # Ouvre le formulaire de configuration
        self.masquer_plante()
        
        # Frame principal de configuration
        config_form = ctk.CTkFrame(self.main_frame, fg_color=self.background_color)
        config_form.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        config_form.grid_columnconfigure(0, weight=1)
        
        # Titre
        titre = ctk.CTkLabel(config_form, text="Configuration de la plante", font=("Helvetica", 38, "bold"), text_color=self.subtitle_color)
        titre.grid(row=0, column=0, pady=(10, 30), padx=20, sticky="w")
        
        # Variables pour stocker les informations
        # self.nom_var = ctk.StringVar(value="")             #surement à supprimer
        self.type_var = ctk.StringVar(value="")              #
        self.capteur_var = ctk.StringVar(value="")           #
        self.date_plantation_var = ctk.StringVar(value="")   #
        self.superficie_var = ctk.StringVar(value="")        #

        nom_ini=self.liste_utilisateurs[self.utilisateur]["plantes"][f"plante {self.no_plante}"]["nom"] #récupérer la base de donnée

        if nom_ini=="Inconnu":# vérifier si c'est la première modification 
            nom_ini=""
        
        type_ini=self.liste_utilisateurs[self.utilisateur]["plantes"][f"plante {self.no_plante}"]["type"] #récupérer le type de la base de donnée

        #initiation des dates possibles
        self.pos_jour=["1","2","3","4","5","6","7","8","9","10","11","12","13","14","15","16","17","18","19","20","21","22","23","24","25","26","27","28","29","30","31"]
        mois=["1","2","3","4","5","6","7","8","9","10","11","12"]
        année=["2025","2024","2023","2022","2021","2020","2019","2018","2017","2016","2015"]

        super_ini=self.liste_utilisateurs[self.utilisateur]["plantes"][f"plante {self.no_plante}"]["superficie"] #récupérer la superficie de la base de donnée

        # date actuelle
        année_ini=self.liste_utilisateurs[self.utilisateur]["plantes"][f"plante {self.no_plante}"]["date_plantation"][0]
        mois_ini=self.liste_utilisateurs[self.utilisateur]["plantes"][f"plante {self.no_plante}"]["date_plantation"][1]
        jour_ini=self.liste_utilisateurs[self.utilisateur]["plantes"][f"plante {self.no_plante}"]["date_plantation"][2]

        capteur_ini=self.liste_utilisateurs[self.utilisateur]["plantes"][f"plante {self.no_plante}"]["capteur"] #récupérer le capteur de la base de donnée
        # Nom
        nom_label = ctk.CTkLabel(config_form, text="Nom de la plante:", font=("Helvetica", 18), text_color=self.subtitle_color)
        nom_label.grid(row=1, column=0, sticky="w", padx=40, pady=(20, 5))
        self.nom_entry = ctk.CTkEntry(config_form, placeholder_text=nom_ini, font=("Helvetica", 16), width=300, height=40, corner_radius=15, fg_color=self.button_text_color, text_color="#000000", border_width=1, border_color="#000000")
        self.nom_entry.grid(row=2, column=0, sticky="w", padx=40, pady=(0, 20))
        
        # Type
        type_label = ctk.CTkLabel(config_form, text="Type de plante:", font=("Helvetica", 18), text_color=self.subtitle_color)
        type_label.grid(row=3, column=0, sticky="w", padx=40, pady=(20, 5))
        self.type_combo = ctk.CTkComboBox(config_form, values=self.liste_types_plantes, font=("Helvetica", 16), dropdown_font=("Helvetica", 16), state="readonly", width=300, height=30, corner_radius=10, fg_color="#ffffff", text_color="#000000", border_color="#A9A9A9")
        self.type_combo.grid(row=4, column=0, sticky="w", padx=40, pady=(0, 20))
        if type_ini!="": #Ne rien faire si le type n'est pas encore configuré
            self.type_combo.set(type_ini)

        # Capteur
        capteur_label = ctk.CTkLabel(config_form, text="Capteur associé:", font=("Helvetica", 18), text_color=self.subtitle_color)
        capteur_label.grid(row=5, column=0, sticky="w", padx=40, pady=(20, 5))
        self.capteur_var = ctk.StringVar(value="ND")
        self.capteur_combo = ctk.CTkComboBox(config_form, values=["1", "2", "3", "4", "5","Non associé"], font=("Helvetica", 16), dropdown_font=("Helvetica", 16), state="readonly", width=130, height=30, corner_radius=10, fg_color="#ffffff", text_color="#000000", border_color="#A9A9A9")
        self.capteur_combo.grid(row=6, column=0, sticky="w", padx=40, pady=(0, 20))
        if capteur_ini!="": # Ne rien faire si le capteur n'est pas encore configuré
            self.capteur_combo.set(capteur_ini)
        
        # Date de plantation
        date_label = ctk.CTkLabel(config_form, text="Date de plantation (AAAA-MM-JJ):", font=("Helvetica", 18), text_color=self.subtitle_color)
        date_label.grid(row=7, column=0, sticky="w", padx=40, pady=(20, 5))

        #choix date de plantation
        self.date_année_combo=ctk.CTkComboBox(config_form, values=année, font=("Helvetica", 16), dropdown_font=("Helvetica", 16), state="readonly", width=100, height=30, corner_radius=10, fg_color="#ffffff", text_color="#000000", border_color="#A9A9A9")
        self.date_année_combo.grid(row=8, column=0, sticky="w", padx=40, pady=(0, 20))
        if année_ini!="": #Ne rien faire si l'année n'est pas encore configuré
            self.date_année_combo.set(année_ini)

        self.date_mois_combo=ctk.CTkComboBox(config_form, values=mois, font=("Helvetica", 16), dropdown_font=("Helvetica", 16), state="readonly", width=75, height=30, corner_radius=10, fg_color="#ffffff", text_color="#000000", border_color="#A9A9A9")
        self.date_mois_combo.grid(row=8, column=0, sticky="w", padx=140, pady=(0, 20))
        if mois_ini!="": #Ne rien faire si le type n'est pas encore configuré
            self.date_mois_combo.set(mois_ini)

        self.date_jour_combo=ctk.CTkEntry(config_form, placeholder_text=jour_ini, font=("Helvetica", 16), width=75, height=30, corner_radius=10, fg_color=self.button_text_color, text_color="#000000", border_width=1, border_color="#000000")
        self.date_jour_combo.grid(row=8, column=0, sticky="w", padx=215, pady=(0, 20))

        # Superficie
        superficie_label = ctk.CTkLabel(config_form, text="Superficie (m²):", font=("Helvetica", 18), text_color=self.subtitle_color)
        superficie_label.grid(row=9, column=0, sticky="w", padx=40, pady=(20, 5))
        self.superficie_entry = ctk.CTkEntry(config_form, placeholder_text=super_ini, font=("Helvetica", 16), width=125, height=30, corner_radius=10, fg_color=self.button_text_color, text_color="#000000", border_width=1, border_color="#000000")
        self.superficie_entry.grid(row=10, column=0, sticky="w", padx=40, pady=(0, 20))
        
        # Boutons
        buttons_frame = ctk.CTkFrame(config_form, fg_color=self.background_color)
        buttons_frame.grid(row=11, column=0, pady=30)
        
        sauvegarder_btn = ctk.CTkButton(buttons_frame, text="Sauvegarder", command=self.sauvegarder_nouvelle_plante, font=("Helvetica", 20, "bold"), corner_radius=15, fg_color="#4CAF50", hover_color="#3e8e41", text_color=self.button_text_color, width=200, height=40)
        sauvegarder_btn.grid(row=0, column=0, padx=10)
        annuler_btn = ctk.CTkButton(buttons_frame, text="Annuler", command=lambda: self.afficher_plante(self.no_plante), font=("Helvetica", 20, "bold"), corner_radius=15, fg_color="#F14156", hover_color="#d32f2f", text_color=self.button_text_color, width=200, height=40)
        annuler_btn.grid(row=0, column=1, padx=10)


    def sauvegarder_nouvelle_plante(self):
        if not self.nom_entry.get():# si il n'y a pas de nom entrer
            if self.liste_utilisateurs[self.utilisateur]["plantes"][f"plante {self.no_plante}"]["nom"]!="Inconnu":
                nom=self.liste_utilisateurs[self.utilisateur]["plantes"][f"plante {self.no_plante}"]["nom"] # si nom déjà configuré
            else:
                self.nom_entry.delete(0, "end") #aucun nom
                self.nom_entry.configure(placeholder_text="Veuillez entrer un nom", placeholder_text_color=self.consigne, font=("Helvetica", 18))
                return 
        else:
            nom=self.nom_entry.get() #sauvegarder le nouveau nom

        if not self.type_combo.get():
            if self.liste_utilisateurs[self.utilisateur]["plantes"][f"plante {self.no_plante}"]["type"]!="":
                type=self.liste_utilisateurs[self.utilisateur]["plantes"][f"plante {self.no_plante}"]["type"] # si type déjà configuré
            else:
                type="Autre" #donné par défault
        else:
            type=self.type_combo.get() #sauvegarder le nouveau type
        
        if not self.capteur_combo.get():
            if self.liste_utilisateurs[self.utilisateur]["plantes"][f"plante {self.no_plante}"]["capteur"]!="":
                capteur=self.liste_utilisateurs[self.utilisateur]["plantes"][f"plante {self.no_plante}"]["capteur"] # si capteur déjà configuré
            else:
                capteur="Non associé" #donné par défault
        else:
            capteur=self.capteur_combo.get() #sauvegarder le nouveau capteur

        if not self.date_année_combo.get():#si il n'y a pas d'années
            if self.liste_utilisateurs[self.utilisateur]["plantes"][f"plante {self.no_plante}"]["date_plantation"][0]!="":
                année=self.liste_utilisateurs[self.utilisateur]["plantes"][f"plante {self.no_plante}"]["date_plantation"][0] # si année déjà configuré
            else:
                return
        else:
            année=self.date_année_combo.get() #sauvegarder le nouveau année

        if not self.date_mois_combo.get():#si il n'y a pas de mois
            if self.liste_utilisateurs[self.utilisateur]["plantes"][f"plante {self.no_plante}"]["date_plantation"][1]!="":
                mois=self.liste_utilisateurs[self.utilisateur]["plantes"][f"plante {self.no_plante}"]["date_plantation"][1] # si mois déjà configuré
            else:
                return
        else:
            mois=self.date_mois_combo.get() #sauvegarder le nouveau mois

        if not self.date_jour_combo.get():# si il n'y a pas de jour entrer
            if self.liste_utilisateurs[self.utilisateur]["plantes"][f"plante {self.no_plante}"]["date_plantation"][2]!="":
                jour=self.liste_utilisateurs[self.utilisateur]["plantes"][f"plante {self.no_plante}"]["date_plantation"][2] # si jour déjà configuré
            else:
                self.date_jour_combo.delete(0, "end") #aucun jour
                self.date_jour_combo.configure(placeholder_text="**", placeholder_text_color=self.consigne, font=("Helvetica", 18))
                return 
        elif self.date_jour_combo.get() in self.pos_jour:
            jour=self.date_jour_combo.get() #sauvegarder le nouveau nom
        else:
            return

        if not self.superficie_entry.get():# si il n'y a pas de superficie entrer
                superf=self.liste_utilisateurs[self.utilisateur]["plantes"][f"plante {self.no_plante}"]["superficie"] # si pas un nombre
        else:
            try:
                superf=float(self.superficie_entry.get()) #sauvegarder le nouveau nom
            
            except ValueError:
                self.superficie_entry.delete(0, "end") #mauvaise réponse
                self.superficie_entry.configure(placeholder_text="Invalide", placeholder_text_color=self.consigne, font=("Helvetica", 18))
                return 
            
        date=[année,mois,jour]
        # Récupérer les données à sauvegarder
        nouvelles_donnees = {
            "nom": nom,
            "type": type,
            "capteur": capteur,
            "date_plantation": date,
            "superficie": superf
        }
        
        # Vérifier si elle existe déjà
        if "plantes" not in self.liste_utilisateurs[self.utilisateur]:
            self.liste_utilisateurs[self.utilisateur]["plantes"] = {}
        
        self.liste_utilisateurs[self.utilisateur]["plantes"][f"plante {self.no_plante}"] = nouvelles_donnees

        with open("users.json", "w") as f:
            json.dump(self.liste_utilisateurs, f, indent=4)
        
        # Mettre à jour le nombre de plantes si nécessaire
        # À supprimer ? 
        self.liste_utilisateurs[self.utilisateur]["nb_plante"] = max(
            self.liste_utilisateurs[self.utilisateur].get("nb_plante", 0),
            self.no_plante
        )
        
        # Recharger la vue avec les nouvelles informations
        self.afficher_plante(self.no_plante)
            
    def afficher_plante_configuree(self): # Affiche les informations d'une plante déjà configurée
        # Configuration de la grille principale
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(0, weight=2)  # Plus d'espace pour les futurs graphiques
        self.main_frame.grid_rowconfigure(1, weight=0)  # Espace pour les boutons en bas
        
        # En-tête avec le nom de la plante
        header_frame = ctk.CTkFrame(self.main_frame, fg_color=self.background_color, height=50)
        header_frame.grid(row=0, column=0, sticky="new", padx=20, pady=(20, 0))
        header_frame.grid_columnconfigure(0, weight=1)
        
        # Titre avec le nom de la plante
        nom_plante = self.plante_courante.get("nom", "Plante sans nom")
        titre = ctk.CTkLabel(header_frame, text=nom_plante, font=("Helvetica", 32, "bold"), text_color=self.subtitle_color)
        titre.grid(row=0, column=0, pady=(60, 25))
        
        # Zone principale pour les futurs graphiques
        self.content_frame = ctk.CTkFrame(self.main_frame, fg_color=self.background_color)
        self.content_frame.grid(row=1, column=0, sticky="nsew", padx=20, pady=10)
        self.content_frame.grid_columnconfigure(0, weight=1)
        
        # Graphiques d'énergie 
        button_voir_energie = ctk.CTkButton(self.content_frame, text="Voir l'énergie absorbée", command=lambda:[self.afficher_graphique_energie(), self.afficher_graph_relations()], font=("Helvetica", 20, "bold"), corner_radius=15, fg_color="#f77a20", hover_color="#c7621a", text_color=self.button_text_color, width=200, height=40)
        button_voir_energie.grid(row=0, column=0, padx=20, pady=(20, 10))

        if self.liste_utilisateurs[self.utilisateur]["plantes"][f"plante {self.no_plante}"]["capteur"]!="Non associé": #Vérification du capteur associé

            #Affichage des informations des prédictions
            button_voir_predictions = ctk.CTkButton(self.content_frame, text="Voir les prédictions", command=self.afficher_prediction, font=("Helvetica", 20, "bold"), corner_radius=15, fg_color="blue", hover_color="dark blue", text_color=self.button_text_color, width=200, height=40)
            button_voir_predictions.grid(row=1, column=0, padx=20, pady=(20, 10))

            #Affichage graphique1
            button_voir_graphique1 = ctk.CTkButton(self.content_frame, text="Voir le graphique des humidités", command=self.afficher_graphique1_les_humidites, font=("Helvetica", 20, "bold"), corner_radius=15, fg_color="violet", hover_color="plum", text_color=self.button_text_color, width=200, height=40)
            button_voir_graphique1.grid(row=2, column=0, padx=20, pady=(20, 10))

            #Affichage graphique2
            button_voir_graphique2 = ctk.CTkButton(self.content_frame, text="Voir le graphique de la température", command=self.afficher_graphique2_temperature, font=("Helvetica", 20, "bold"), corner_radius=15, fg_color="blueviolet", hover_color="indigo", text_color=self.button_text_color, width=200, height=40)
            button_voir_graphique2.grid(row=3, column=0, padx=20, pady=(20, 10))

            #Affichage graphique3
            button_voir_graphique3 = ctk.CTkButton(self.content_frame, text="Voir le graphique de la luminosité", command=self.afficher_graphique3_luminosite, font=("Helvetica", 20, "bold"), corner_radius=15, fg_color="darkturquoise", hover_color="darkcyan", text_color=self.button_text_color, width=200, height=40)
            button_voir_graphique3.grid(row=4, column=0, padx=20, pady=(20, 10))

            #Affichage d'une nouvelle page pour les graphiques de dérivées
            button_voir_graphiques_deriv = ctk.CTkButton(self.content_frame, text="Voir les graphiques du comportement de la plante", command=self.nouvelle_page_derivees, font=("Helvetica", 20, "bold"), corner_radius=15, fg_color="cornflowerblue", hover_color="royalblue", text_color=self.button_text_color, width=200, height=40)
            button_voir_graphiques_deriv.grid(row=5, column=0, padx=20, pady=(20, 10))

            #Affichage tableau dataframe résumé
            button_tableau = ctk.CTkButton(self.content_frame, text="Voir le tableau résumé", command=self.afficher_tableau_resume, font=("Helvetica", 20, "bold"), corner_radius=15, fg_color="lightskyblue", hover_color="steelblue", text_color=self.button_text_color, width=200, height=40)
            button_tableau.grid(row=6, column=0, padx=20, pady=(20, 10))


        if self.liste_utilisateurs[self.utilisateur]["plantes"][f"plante {self.no_plante}"]["capteur"]=="Non associé": #Vérification du capteur associé
            capt_u="! Aucun capteur n'est associé à cette plante !"
            coul_u="red"
        else:
            capt_u=f"La plante {self.plante_courante.get('nom')} est associée au capteur {self.plante_courante.get('capteur')}"
            coul_u="lime"

        #Afficher si un capteur est asocié ou non
        Capteur = ctk.CTkLabel(self.content_frame, text=capt_u, font=("Helvetica", 15, "bold"), text_color=coul_u)
        Capteur.grid(row=7, column=0, padx=20, pady=(20, 10))
        
        # Barre de boutons en bas
        button_bar = ctk.CTkFrame(self.main_frame, fg_color=self.background_color, height=60)
        button_bar.grid(row=2, column=0, sticky="sew", padx=20, pady=(10, 20))
        button_bar.grid_columnconfigure((0,1,2,3), weight=1)
        
        # Bouton retour
        self.retour_btn = ctk.CTkButton(button_bar, text="← Retour", command=lambda:[self.close_graphique(), self.retour_accueil()],font=("Helvetica", 16, "bold"), width=150, height=35, corner_radius=15, fg_color="#AAAAAA", hover_color="#CCCCCC", text_color=self.button_text_color)
        self.retour_btn.grid(row=0, column=0, padx=10, pady=10, sticky="w")
        
        # Bouton modification
        self.modifier_btn = ctk.CTkButton(button_bar, text="Modifier", command=self.modifier_plante, font=("Helvetica", 16, "bold"), width=150, height=35, corner_radius=15, fg_color="#4CAF50", hover_color="#3e8e41", text_color=self.button_text_color)
        self.modifier_btn.grid(row=0, column=1, padx=10, pady=10)
        
        # Bouton supprimer
        self.supprimer_btn = ctk.CTkButton(button_bar, text="Supprimer la plante", command=self.confirmer_suppression,font=("Helvetica", 16, "bold"), width=150, height=35, corner_radius=15, fg_color="#F14156", hover_color="#d32f2f", text_color=self.button_text_color)
        self.supprimer_btn.grid(row=0, column=3, padx=10, pady=10, sticky="e")

    def confirmer_suppression(self): # Affiche une fenêtre de confirmation avant de supprimer une plante
        self.confirmation_window = ctk.CTkToplevel(self.master)
        self.confirmation_window.title("Confirmation")
        self.confirmation_window.attributes('-topmost', True)

        # Centrer la fenêtre
        self.confirmation_window.geometry("400x200")
        self.confirmation_window.update_idletasks()
        x = (self.confirmation_window.winfo_screenwidth() // 2) - (400 // 2)
        y = (self.confirmation_window.winfo_screenheight() // 2) - (200 // 2)
        self.confirmation_window.geometry(f'+{x}+{y}')

        # Message
        label = ctk.CTkLabel(self.confirmation_window, text=f"Êtes-vous sûr de vouloir supprimer\nla plante {self.plante_courante.get('nom', '')} ?", font=("Helvetica", 16))
        label.pack(pady=30)

        # Boutons
        buttons_frame = ctk.CTkFrame(self.confirmation_window, fg_color="transparent")
        buttons_frame.pack(pady=20)

        oui_btn = ctk.CTkButton(buttons_frame, text="Oui", command=self.supprimer_plante, font=("Helvetica", 16), corner_radius=15, fg_color="#F14156", hover_color="#d32f2f", text_color=self.button_text_color, width=100)
        oui_btn.grid(row=0, column=0, padx=10)

        non_btn = ctk.CTkButton(buttons_frame, text="Non", command=self.confirmation_window.destroy, font=("Helvetica", 16), corner_radius=15, fg_color="#AAAAAA", hover_color="#CCCCCC", text_color=self.button_text_color, width=100)
        non_btn.grid(row=0, column=1, padx=10)
        
    def supprimer_plante(self):
        # Supprime la plante et réindexe les autres si besoins
        utilisateur_data = self.liste_utilisateurs.get(self.utilisateur, {})
        plantes_data = utilisateur_data.get("plantes", {})

        if f"plante {self.no_plante}" in plantes_data:
            del plantes_data[f"plante {self.no_plante}"]

            # Réindexation des plantes restantes pour éviter les "trous"
            nouvelles_plantes = {}
            index = 1  # Toujours commencer par "plante 1"
            for key in sorted(plantes_data.keys(), key=lambda x: int(x.split(" ")[1])):  # Tri par numéro
                nouvelles_plantes[f"plante {index}"] = plantes_data[key]
                index += 1

            # Met à jour les données utilisateur
            utilisateur_data["plantes"] = nouvelles_plantes
            utilisateur_data["nb_plante"] = len(nouvelles_plantes)

            # Sauvegarde dans users.json
            with open("users.json", "w") as f:
                json.dump(self.liste_utilisateurs, f, indent=4)

        # Fermer la fenêtre de confirmation si ouverte
        if hasattr(self, "confirmation_window"):
            self.confirmation_window.destroy()
        self.retour_accueil()
    
    def afficher_graphique_energie(self):
        # Récupération de la superficie
        if self.plante_courante.get("superficie") != "":
            superficie = float(self.plante_courante.get("superficie"))
        else:
            superficie = 0.01
        
        # Nettoyage du frame de contenu avant d'afficher le graphique
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        self.retour_btn.grid_forget()
        self.modifier_btn.grid_forget()
        self.supprimer_btn.grid_forget()
        
        # Création du graphique
        self.energie_plante = Energie(superficie)
        fig, ax = plt.subplots(figsize=(5, 4))
        self.energie_plante.afficher_graphique_resultats(ax, fig)
        
        # Affichage du graphique
        canvas = FigureCanvasTkAgg(fig, master=self.content_frame)
        canvas.draw()
        canvas.get_tk_widget().grid(row=0, column=0, padx=10, pady=(10, 30))
        
        # Ajouter un bouton retour sous le graphique
        retour_btn = ctk.CTkButton(self.content_frame, text="Retour à la plante", command=lambda:[canvas.get_tk_widget().grid_remove(), self.close_graphique(), self.afficher_plante_configuree()], font=("Helvetica", 16, "bold"), corner_radius=15, fg_color="#AAAAAA", hover_color="#CCCCCC", text_color=self.button_text_color, width=200, height=35)
        retour_btn.grid(row=1, column=0, padx=10, pady=10)

    def close_graphique(self):  # Ferme les figures matplotlib
        # Fermer proprement les canvases si présents
        try:
            for widget in self.content_frame.winfo_children():
                if hasattr(widget, 'get_tk_widget'):
                    widget.get_tk_widget().destroy()
                    
            import matplotlib.pyplot as plt
            plt.close('all')  # Ferme toutes les figures ouvertes
            
            # Libérer les ressources du graph s'il existe. Aidé par l'IA
            if hasattr(self, 'graph'):
                del self.graph
            
        except Exception as e:
            print(f"Erreur lors de la fermeture du graphique: {e}")

    def afficher_graph_relations(self):  
        self.graph = Graph()
        self.graph.cree_graph_sujet_1()  # Créer le graphe spécifique
        
        # Récupération de la figure du graphe
        fig = self.graph.creer_figure_graph(title="Relations entre capteurs")
        
        # Affichage du graphique
        canvas = FigureCanvasTkAgg(fig, master=self.content_frame)
        canvas.draw()
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.grid(row=0, column=1, padx=10, pady=10)
        
        # Stocker une référence au widget canvas pour pouvoir utiliser grid_remove après
        self.graph_canvas_widget = canvas_widget

        # Ajouter le texte
        self.afficher_informations()
    
    def afficher_informations(self):
        # Ajout des informations texttuels sur le graphique d'énergie ainsi que sur le graph de relations
        # Graphique d'énergie
        info_energie = self.energie_plante.get_resultats_energie()
        info_energie_label = ctk.CTkLabel(self.content_frame, text=f"Énergie totale absorbée sur 24h : {info_energie['energie_totale']/1000:.1f} kJoules", font=("Helvetica", 18), text_color=self.subtitle_color)
        info_energie_label.grid(row=2, column=0, columnspan=2, padx=10, pady=(30, 0))
        
        # Graph de relations
        if self.liste_utilisateurs[self.utilisateur]["plantes"][f"plante {self.no_plante}"]["capteur"] != "Non associé":
            no_capteur = int(self.liste_utilisateurs[self.utilisateur]["plantes"][f"plante {self.no_plante}"]["capteur"])
            info_capteur = self.graph.get_info_capteur(no_capteur)
            if info_capteur != -1:
                parametre = info_capteur['Type']
                if parametre == "lumière":
                    parametre = "La lumière est le facteur qui influence le plus"
                elif parametre == "ambiant":
                    parametre = "La température et l'humidité ambiante sont les facteurs qui influencent le plus"

                info_capteur_label = ctk.CTkLabel(self.content_frame, text=f"Capteur de la plante {no_capteur} : {parametre} la plante avec un facteur de {abs(info_capteur['Corrélation'])}", font=("Helvetica", 18), text_color=self.subtitle_color)
                info_capteur_label.grid(row=3, column=0, columnspan=2, padx=10, pady=(10, 0))
            else:
                info_capteur_label = ctk.CTkLabel(self.content_frame, text="Aucun capteur spécifique associé.", font=("Helvetica", 18), text_color=self.subtitle_color)
                info_capteur_label.grid(row=3, column=0, columnspan=2, padx=10, pady=(10, 0))
        else:
            info_capteur_label = ctk.CTkLabel(self.content_frame, text="Aucun capteur spécifique associé.", font=("Helvetica", 18), text_color=self.subtitle_color)
            info_capteur_label.grid(row=3, column=0, columnspan=2, padx=10, pady=(10, 0))

        # Mettre à jour le bouton retour pour fermer les deux graphiques
        retour_btn = self.content_frame.winfo_children()[1]  # Récupère le bouton retour créé dans afficher_graphique_energie
        retour_btn.grid_forget() 
        retour_btn.grid(row=4, column=0, columnspan=2, padx=10, pady=(150, 0))  # Repositionner centré sous les deux graphiques
        retour_btn.configure(command=self.retour_a_plante_config)

    def retour_a_plante_config(self):
        # Détruire complètement tous les widgets du content_frame
        try:
            # Détruire tous les widgets dans le content_frame
            for widget in self.content_frame.winfo_children():
                widget.destroy()
            
            # Fermer les figures matplotlib
            plt.close('all')
            
            # Libérer les ressources du graph s'il existe. Aidé par l'IA
            if hasattr(self, 'graph'):
                del self.graph
        except Exception as e:
            print(f"Erreur lors de la suppression des graphiques: {e}")
        
        self.content_frame.destroy()  # Détruire complètement le frame
        self.afficher_plante_configuree()  # Recréer toute l'interface

    def afficher_prediction(self):
        if self.liste_utilisateurs[self.utilisateur]["plantes"][f"plante {self.no_plante}"]["capteur"]=="Non associé":
            return ## À ajouter à l'affichage des tableaux
         # Frame central pour la configuration
        self.config_frame = ctk.CTkFrame(self.main_frame, fg_color=self.background_color)
        self.config_frame.grid(row=1, column=0, sticky="nsew", padx=20, pady=20)
        self.config_frame.grid_columnconfigure(0, weight=1)

        #Récupérations des prédictions
        humi=Predictions.humidite_du_sol(self,load_data_from_gist(),self.liste_utilisateurs[self.utilisateur]["plantes"][f"plante {self.no_plante}"]["capteur"])
        humi_am=Predictions.humidite_ambiante(self,load_data_from_gist(),self.liste_utilisateurs[self.utilisateur]["plantes"][f"plante {self.no_plante}"]["capteur"])
        temp=Predictions.temperature(self,load_data_from_gist(),self.liste_utilisateurs[self.utilisateur]["plantes"][f"plante {self.no_plante}"]["capteur"])

          # Récupération de la superficie
        if self.plante_courante.get("superficie") != "":
            superficie = float(self.plante_courante.get("superficie"))
        else:
            superficie = 0.01
        
        # Nettoyage du frame de contenu avant d'afficher le graphique
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        self.retour_btn.grid_forget()
        self.modifier_btn.grid_forget()
        self.supprimer_btn.grid_forget()

        #Gestion des couleurs:

        #choix des couleurs
        choix1=["sandybrown","saddlebrown"]
        choix2=["deepskyblue","steelblue"]
        choix3=["red","darkred"]
        
        # initialisation des couleurs pour chaque prédictions
        coul_humi=[choix1[0],choix1[0],choix1[0]]
        coul_humi_amb=[choix2[0],choix2[0],choix2[0]]
        coul_temp=[choix3[0],choix3[0],choix3[0]]        

        # Plus grosse couleur selon la prédiction la plus haute pour
            # l'humidité du sol
        if humi[0]>=humi[1] and humi[0]>=humi[2]:
            coul_humi[0]=choix1[1]
        if humi[1]>=humi[0] and humi[1]>=humi[2]:
            coul_humi[1]=choix1[1]
        if humi[2]>=humi[1] and humi[2]>=humi[0]:
            coul_humi[2]=choix1[1]

            # l'humidité ambiante
        if humi_am[0]>=humi_am[1] and humi_am[0]>=humi_am[2]:
            coul_humi_amb[0]=choix2[1]
        if humi_am[1]>=humi_am[0] and humi_am[1]>=humi_am[2]:
            coul_humi_amb[1]=choix2[1]
        if humi_am[2]>=humi_am[1] and humi_am[2]>=humi_am[0]:
            coul_humi_amb[2]=choix2[1]

            # la température
        if temp[0]>=temp[1] and temp[0]>=temp[2]:
            coul_temp[0]=choix3[1]
        if temp[1]>=temp[0] and temp[1]>=temp[2]:
            coul_temp[1]=choix3[1]
        if temp[2]>=temp[1] and temp[2]>=temp[0]:
            coul_temp[2]=choix3[1]

        # humidité du sol
        humidite = ctk.CTkLabel(self.config_frame, text="L'humidité du sol a :", font=("Helvetica", 20, "bold"), text_color="maroon")
        humidite.grid(row=0, column=0, padx=10, pady=10)
        humidite = ctk.CTkLabel(self.config_frame, text=f"{humi[0]:.1f}% de chance d'augmenter", font=("Helvetica", 15, "bold"), text_color=coul_humi[0])
        humidite.grid(row=1, column=0, padx=10, pady=10)
        humidite = ctk.CTkLabel(self.config_frame, text=f"{humi[1]:.1f}% de chance de diminuer", font=("Helvetica", 15, "bold"), text_color=coul_humi[1])
        humidite.grid(row=2, column=0, padx=10, pady=10)
        humidite = ctk.CTkLabel(self.config_frame, text=f"{humi[2]:.1f}% de chance de ne pas varier", font=("Helvetica", 15, "bold"), text_color=coul_humi[2])
        humidite.grid(row=3, column=0, padx=10, pady=10)

        # humidité ambiante
        humidite_a = ctk.CTkLabel(self.config_frame, text="L'humidité ambiante a :", font=("Helvetica", 20, "bold"), text_color="dodgerblue")
        humidite_a.grid(row=0, column=1, padx=10, pady=10)
        humidite_a = ctk.CTkLabel(self.config_frame, text=f"{humi_am[0]:.1f}% de chance d'augmenter", font=("Helvetica", 15, "bold"), text_color=coul_humi_amb[0])
        humidite_a.grid(row=1, column=1, padx=10, pady=10)
        humidite_a = ctk.CTkLabel(self.config_frame, text=f"{humi_am[1]:.1f}% de chance de diminuer", font=("Helvetica", 15, "bold"), text_color=coul_humi_amb[1])
        humidite_a.grid(row=2, column=1, padx=10, pady=10)
        humidite_a = ctk.CTkLabel(self.config_frame, text=f"{humi_am[2]:.1f}% de chance de ne pas varier", font=("Helvetica", 15, "bold"), text_color=coul_humi_amb[2])
        humidite_a.grid(row=3, column=1, padx=10, pady=10)

        # température
        tempe = ctk.CTkLabel(self.config_frame, text="La température a :", font=("Helvetica", 20, "bold"), text_color="crimson")
        tempe.grid(row=0, column=2, padx=10, pady=10)
        tempe = ctk.CTkLabel(self.config_frame, text=f"{temp[0]:.1f}% de chance d'augmenter", font=("Helvetica", 15, "bold"), text_color=coul_temp[0])
        tempe.grid(row=1, column=2, padx=10, pady=10)
        tempe = ctk.CTkLabel(self.config_frame, text=f"{temp[1]:.1f}% de chance de diminuer", font=("Helvetica", 15, "bold"), text_color=coul_temp[1])
        tempe.grid(row=2, column=2, padx=10, pady=10)
        tempe = ctk.CTkLabel(self.config_frame, text=f"{temp[2]:.1f}% de chance de ne pas varier", font=("Helvetica", 15, "bold"), text_color=coul_temp[2])
        tempe.grid(row=3, column=2, padx=10, pady=10)


        # Ajouter un bouton retour sous le graphique
        retour_btn = ctk.CTkButton(self.config_frame, text="Retour à la plante", command=lambda:[self.config_frame.grid_remove(),self.afficher_plante_configuree()], font=("Helvetica", 16, "bold"), corner_radius=15, fg_color="#AAAAAA", hover_color="#CCCCCC", text_color=self.button_text_color, width=200, height=35)
        retour_btn.grid(row=4, column=1, padx=10, pady=20)

        
        
    def retour_accueil(self):
        self.masquer_plante()
        self.accueil.afficher_accueil(self.utilisateur)
    
    def setup_colors(self):
        self.background_color = "#fffcfc"
        self.subtitle_color = "#4D4D4D"
        self.consigne = "#F14156"
        self.button_text_color = "#FFFFFF"
        
    def capteur_acces(self):
        self.no_capteur = self.plante_courante["capteur"]
        
        if self.no_capteur:
            try:
                capteur_int = int(self.no_capteur)
                if capteur_int == 1:
                    laplante = "Capteur 1"
                elif capteur_int == 2:
                    laplante = "Capteur 2"
                elif capteur_int == 3:
                    laplante = "Capteur 3"
                elif capteur_int == 4:
                    laplante = "Capteur 4"
                elif capteur_int == 5:
                    laplante = "Capteur 5"
                else:
                    laplante = None
            except ValueError:
                print("Erreur : Capteur invalide.")
                laplante = None
        else:
            print("Erreur : Aucun capteur sélectionné.")
            laplante = None
        
        if laplante is None:
            print("Erreur : Capteur inconnu.")

        return laplante

    def afficher_graphique1_les_humidites(self):
        if self.liste_utilisateurs[self.utilisateur]["plantes"][f"plante {self.no_plante}"]["capteur"]=="Non associé":
            return
        laplante = self.capteur_acces()
        deriv = Derivee(laplante)

        # Nettoyage du frame de contenu avant d'afficher le graphique
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        self.retour_btn.grid_forget()
        self.modifier_btn.grid_forget()
        self.supprimer_btn.grid_forget()
        
        # Création et affichage du graphique
        graph1 = deriv.graphique1_les_humidites(laplante)
        self.canvas = FigureCanvasTkAgg(graph1, master=self.content_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().grid(row=1, column=0, pady=(10,10))
        
        # Ajouter un bouton retour sous le graphique
        retour_btn = ctk.CTkButton(self.content_frame, text="Retour à la plante", command=lambda:[self.canvas.get_tk_widget().grid_remove(),self.afficher_plante_configuree()], font=("Helvetica", 16, "bold"), corner_radius=15, fg_color="#AAAAAA", hover_color="#CCCCCC", text_color=self.button_text_color, width=200, height=35)
        retour_btn.grid(row=2, column=0, padx=10, pady=20)



    def afficher_graphique2_temperature(self):
        if self.liste_utilisateurs[self.utilisateur]["plantes"][f"plante {self.no_plante}"]["capteur"]=="Non associé":
            return
        laplante = self.capteur_acces()
        deriv = Derivee(laplante)

        # Nettoyage du frame de contenu avant d'afficher le graphique
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        self.retour_btn.grid_forget()
        self.modifier_btn.grid_forget()
        self.supprimer_btn.grid_forget()
        
        # Création et affichage du graphique
        graph2 = deriv.graphique2_temperature(laplante)
        self.canvas = FigureCanvasTkAgg(graph2, master=self.content_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().grid(row=1, column=0, pady=(10,10))
        
        # Ajouter un bouton retour sous le graphique
        retour_btn = ctk.CTkButton(self.content_frame, text="Retour à la plante", command=lambda:[self.canvas.get_tk_widget().grid_remove(),self.afficher_plante_configuree()], font=("Helvetica", 16, "bold"), corner_radius=15, fg_color="#AAAAAA", hover_color="#CCCCCC", text_color=self.button_text_color, width=200, height=35)
        retour_btn.grid(row=2, column=0, padx=10, pady=20)


    def afficher_graphique3_luminosite(self):
        if self.liste_utilisateurs[self.utilisateur]["plantes"][f"plante {self.no_plante}"]["capteur"]=="Non associé":
            return
        laplante = self.capteur_acces()
        deriv = Derivee(laplante)

        # Nettoyage du frame de contenu avant d'afficher le graphique
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        self.retour_btn.grid_forget()
        self.modifier_btn.grid_forget()
        self.supprimer_btn.grid_forget()
        
        # Création et affichage du graphique
        graph3 = deriv.graphique3_luminosite(laplante)
        self.canvas = FigureCanvasTkAgg(graph3, master=self.content_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().grid(row=1, column=0, pady=(10,10))
        
        # Ajouter un bouton retour sous le graphique
        retour_btn = ctk.CTkButton(self.content_frame, text="Retour à la plante", command=lambda:[self.canvas.get_tk_widget().grid_remove(),self.afficher_plante_configuree()], font=("Helvetica", 16, "bold"), corner_radius=15, fg_color="#AAAAAA", hover_color="#CCCCCC", text_color=self.button_text_color, width=200, height=35)
        retour_btn.grid(row=2, column=0, padx=10, pady=20)


    def nouvelle_page_derivees(self):
        if self.liste_utilisateurs[self.utilisateur]["plantes"][f"plante {self.no_plante}"]["capteur"]=="Non associé":
            return
        # Nettoyage du frame de contenu avant d'afficher le graphique
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        self.retour_btn.grid_forget()
        self.modifier_btn.grid_forget()
        self.supprimer_btn.grid_forget()

        #Affichage graphique4
        button_voir_graphique4 = ctk.CTkButton(self.content_frame, text="Voir le comportement de l'humidité du sol", command=self.afficher_graph4_deriv_humidite_sol, font=("Helvetica", 20, "bold"), corner_radius=15, fg_color="lightcoral", hover_color="indianred", text_color=self.button_text_color, width=200, height=40)
        button_voir_graphique4.grid(row=1, column=0, padx=20, pady=(20, 10))

        #Affichage graphique5
        button_voir_graphique5 = ctk.CTkButton(self.content_frame, text="Voir le comportement de l'humidité ambiante", command=self.afficher_graph5_deriv_humidite_ambiante, font=("Helvetica", 20, "bold"), corner_radius=15, fg_color="palegreen", hover_color="darkseagreen", text_color=self.button_text_color, width=200, height=40)
        button_voir_graphique5.grid(row=2, column=0, padx=20, pady=(20, 10))

        #Affichage graphique6
        button_voir_graphique6 = ctk.CTkButton(self.content_frame, text="Voir le comportement de la température", command=self.afficher_graph6_deriv_temperature, font=("Helvetica", 20, "bold"), corner_radius=15, fg_color="goldenrod", hover_color="darkgoldenrod", text_color=self.button_text_color, width=200, height=40)
        button_voir_graphique6.grid(row=3, column=0, padx=20, pady=(20, 10))

        #Affichage graphique7
        button_voir_graphique7 = ctk.CTkButton(self.content_frame, text="Voir le comportement de la luminosité", command=self.afficher_graph7_deriv_luminosite, font=("Helvetica", 20, "bold"), corner_radius=15, fg_color="pink", hover_color="palevioletred", text_color=self.button_text_color, width=200, height=40)
        button_voir_graphique7.grid(row=4, column=0, padx=20, pady=(20, 10))

        
        # Ajouter un bouton retour à la plante
        retour_bouton = ctk.CTkButton(self.content_frame, text="Retour à la plante", command=lambda:[self.afficher_plante_configuree()], font=("Helvetica", 16, "bold"), corner_radius=15, fg_color="#AAAAAA", hover_color="#CCCCCC", text_color=self.button_text_color)
        retour_bouton.grid(row=10, column=0, padx=10, pady=20)


    def afficher_graph4_deriv_humidite_sol(self):
        laplante = self.capteur_acces()
        deriv = Derivee(laplante)

        # Nettoyage du frame de contenu avant d'afficher le graphique
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        self.retour_btn.grid_forget()
        self.modifier_btn.grid_forget()
        self.supprimer_btn.grid_forget()
        
        # Création et affichage du graphique
        graph4 = deriv.graphique4_derivee_humidite_sol(laplante)
        self.canvas = FigureCanvasTkAgg(graph4, master=self.content_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().grid(row=1, column=0, pady=(10,10))
        
        # Ajouter un bouton retour sous le graphique
        retour_btn4 = ctk.CTkButton(self.content_frame, text="Retour", command=lambda:[self.canvas.get_tk_widget().grid_remove(),self.nouvelle_page_derivees()], font=("Helvetica", 16, "bold"), corner_radius=15, fg_color="#AAAAAA", hover_color="#CCCCCC", text_color=self.button_text_color, width=200, height=35)
        retour_btn4.grid(row=2, column=0, padx=10, pady=20)



    def afficher_graph5_deriv_humidite_ambiante(self):
        laplante = self.capteur_acces()
        deriv = Derivee(laplante)

        # Nettoyage du frame de contenu avant d'afficher le graphique
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        self.retour_btn.grid_forget()
        self.modifier_btn.grid_forget()
        self.supprimer_btn.grid_forget()
        
        # Création et affichage du graphique
        graph5 = deriv.graphique5_derivee_humidite_ambiante(laplante)
        self.canvas = FigureCanvasTkAgg(graph5, master=self.content_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().grid(row=1, column=0, pady=(10,10))
        
        # Ajouter un bouton retour sous le graphique
        retour_btn5 = ctk.CTkButton(self.content_frame, text="Retour", command=lambda:[self.canvas.get_tk_widget().grid_remove(),self.nouvelle_page_derivees()], font=("Helvetica", 16, "bold"), corner_radius=15, fg_color="#AAAAAA", hover_color="#CCCCCC", text_color=self.button_text_color, width=200, height=35)
        retour_btn5.grid(row=2, column=0, padx=10, pady=20)


    def afficher_graph6_deriv_temperature(self):
        laplante = self.capteur_acces()
        deriv = Derivee(laplante)

        # Nettoyage du frame de contenu avant d'afficher le graphique
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        self.retour_btn.grid_forget()
        self.modifier_btn.grid_forget()
        self.supprimer_btn.grid_forget()
        
        # Création et affichage du graphique
        graph6 = deriv.graphique6_derivee_temperature(laplante)
        self.canvas = FigureCanvasTkAgg(graph6, master=self.content_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().grid(row=1, column=0, pady=(10,10))
        
        # Ajouter un bouton retour sous le graphique
        retour_btn6 = ctk.CTkButton(self.content_frame, text="Retour", command=lambda:[self.canvas.get_tk_widget().grid_remove(),self.nouvelle_page_derivees()], font=("Helvetica", 16, "bold"), corner_radius=15, fg_color="#AAAAAA", hover_color="#CCCCCC", text_color=self.button_text_color, width=200, height=35)
        retour_btn6.grid(row=2, column=0, padx=10, pady=20)
        
    def afficher_graph7_deriv_luminosite(self):
        laplante = self.capteur_acces()
        deriv = Derivee(laplante)

        # Nettoyage du frame de contenu avant d'afficher le graphique
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        self.retour_btn.grid_forget()
        self.modifier_btn.grid_forget()
        self.supprimer_btn.grid_forget()
        
        # Création et affichage du graphique
        graph7 = deriv.graphique7_derivee_luminosite(laplante)
        self.canvas = FigureCanvasTkAgg(graph7, master=self.content_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().grid(row=1, column=0, pady=(10,10))
        
        # Ajouter un bouton retour sous le graphique
        retour_btn7 = ctk.CTkButton(self.content_frame, text="Retour", command=lambda:[self.canvas.get_tk_widget().grid_remove(),self.nouvelle_page_derivees()], font=("Helvetica", 16, "bold"), corner_radius=15, fg_color="#AAAAAA", hover_color="#CCCCCC", text_color=self.button_text_color, width=200, height=35)
        retour_btn7.grid(row=2, column=0, padx=10, pady=20)

    def afficher_tableau_resume(self):
        if self.liste_utilisateurs[self.utilisateur]["plantes"][f"plante {self.no_plante}"]["capteur"]=="Non associé":
            return
        laplante = self.capteur_acces()
        deriv = Derivee(laplante)

        # Nettoyage du frame de contenu avant d'afficher le tableau
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        self.retour_btn.grid_forget()
        self.modifier_btn.grid_forget()
        self.supprimer_btn.grid_forget()
    
        # Nouveau frame pour le tableau
        self.table_frame = ctk.CTkFrame(self.content_frame)
        self.table_frame.grid(row=0, column=0, padx=20, pady=(20, 10), sticky="w")

        #Création et affichage du tableau
        tableau_données = deriv.tableau_resume(self.table_frame, laplante)

        #conditions dérivées
        df_derivees_moy = tableau_données.iloc[2, 1:]
        i=0
        for col, valeur in df_derivees_moy.items():
            i=i+1
            if valeur == 0:
                self.infos1_label = ctk.CTkLabel(self.content_frame, text=(f"{col} n'a en moyenne pas varié."), text_color="orange")
                self.infos1_label.grid(row=10+i, column=0, columnspan=2, pady=10, sticky="n")
            elif valeur > 1 :
                self.infos_label = ctk.CTkLabel(self.content_frame, text=(f"{col} a en moyenne augmenté."), text_color="orange")
                self.infos_label.grid(row=10+i, column=0, columnspan=2, pady=10, sticky="n")
            elif valeur > 0 and valeur < 1:
                self.infos_label = ctk.CTkLabel(self.content_frame, text=(f"{col} a en moyenne légèrement augmenté."), text_color="orange")
                self.infos_label.grid(row=10+i, column=0, columnspan=2, pady=10, sticky="n")
            elif valeur < 0 and valeur > -1:
                self.infos_label = ctk.CTkLabel(self.content_frame, text=(f"{col} a en moyenne légèrement diminué."), text_color="orange")
                self.infos_label.grid(row=10+i, column=0, columnspan=2, pady=10, sticky="n")
            elif valeur > 50:
                self.infos_label = ctk.CTkLabel(self.content_frame, text=(f"{col} a en moyenne grandement augmenté."), text_color="orange")
                self.infos_label.grid(row=10+i, column=0, columnspan=2, pady=10, sticky="n")
            elif valeur < -50:
                self.infos_label = ctk.CTkLabel(self.content_frame, text=(f"{col} a en moyenne grandement diminué."), text_color="orange")
                self.infos_label.grid(row=10+i, column=0, columnspan=2, pady=10, sticky="n")
            elif valeur < -1 :
                self.infos_label = ctk.CTkLabel(self.content_frame, text=(f"{col} a en moyenne diminué"), text_color="orange")
                self.infos_label.grid(row=10+i, column=0, columnspan=2, pady=10, sticky="n")

        # Ajouter un bouton retour sous le tableau et les infos
        retour_btn = ctk.CTkButton(self.content_frame, text="Retour à la plante", command=lambda: (self.table_frame.destroy(), self.afficher_plante_configuree()), font=("Helvetica", 16, "bold"), corner_radius=15, fg_color="#AAAAAA", hover_color="#CCCCCC", text_color=self.button_text_color, width=200, height=35)
        retour_btn.grid(row=20, column=0, padx=10, pady=20)
        