# energie.py : implémentation scientifique

"""
Auteur : Émile Gagnon
Date : 2025-05-25
Description : Présentation d’un extrait de code

Démarche suivie :

1. Récolter les valeurs d'écrairement (en lux et selon les spectres) et de l'aire de la surface éclairé de la plante (en m^2) 

2. Conversion du flux lumineux en puissance optique (P, en watts)

3. Calculer le nombre de photons émis par seconde avec l’énergie d’un photon, 
   sachant qu'il sont répartie dans différents canaux de spectre visible : 

Violet_415nm : 405-425nm  
Indigo_445nm : 435-455nm
Bleu_480nm   : 470-490nm
Cyan_515nm   : 505-525nm
Vert_555nm   : 545-565nm
Jaune_590nm  : 580-600nm
Orange_630nm : 620-640nm
Rouge_680nm  : 670-690nm
Clear (sans filtre): ... (lux)

4. Calculer l'énergie totale absorbée par une plante sur une durée t.

Note : Les valeurs de l'écrairement et de la répartitions des canaux sont acutalisés au 15 minutes.
       Donc, la durée t est de 15 min et s'addisionne sur une journée avec le temps.
       Le fichier data est un csv regroupant 96 prises de données, soit un historique de 24 heures.
"""

# energie.py : implémentation scientifique
import sys
import os
import matplotlib.pyplot as plt
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from load_fichier_csv import load_data_limited

class Energie:
    def __init__(self, surface_plante):
        self.surface = surface_plante # Surface éclairée de la plante en m²
        self.setup_variables()
        self.calculer_energie()
    
    def setup_variables(self):
        # Récupère les données du csv
        self.data = load_data_limited(['Clear','Violet_415nm', 'Indigo_445nm', 'Bleu_480nm', 'Cyan_515nm','Vert_555nm', 'Jaune_590nm', 'Orange_630nm', 'Rouge_680nm'])

        # Constantes physiques
        self.h = 6.62607015e-34 # Constantes de Planck
        self.c = 299792458      # Vitesse de la lumière (dans le vide, en m/s)
        self.delta_t = 15 * 60  # Durée entre deux mesures (15 minutes en secondes)
        
        # Définition des plages de longueurs d'onde (nm) pour chaque canal
        self.plage_lambda = { 
            'Violet_415nm': (405, 425),
            'Indigo_445nm': (435, 455),
            'Bleu_480nm': (470, 490),
            'Cyan_515nm': (505, 525),
            'Vert_555nm': (545, 565),
            'Jaune_590nm': (580, 600),
            'Orange_630nm': (620, 640),
            'Rouge_680nm': (670, 690)
        }

        # Facteurs de conversion spécifiques pour chaque canal spectral
        # Note : Ces valeurs sont approximatives et basées sur l'efficacité lumineuse relative
        self.lux_en_wat_selon_spectre = {
            'Violet_415nm': 1/27,    # 415 nm : faible
            'Indigo_445nm': 1/116,   # 445 nm : faible
            'Bleu_480nm': 1/240,     # 480 nm : moyenne
            'Cyan_515nm': 1/510,     # 515 nm : élevée
            'Vert_555nm': 1/680,     # 555 nm : maximale
            'Jaune_590nm': 1/520,    # 590 nm : élevée
            'Orange_630nm': 1/220,   # 630 nm : moyenne
            'Rouge_680nm': 1/73      # 680 nm : faible
        }
    
    def calculer_energie_photon(self, longueur_onde):
        # Calcule l'énergie d'un photon à une longueur d'onde donnée
        longueur_onde_m = longueur_onde * 1e-9
        return (self.h * self.c) / longueur_onde_m # E = h*c/λ
    
    def calculer_energie(self):
        # Calcule l'énergie totale absorbée par la plante sur 24 heures 
        self.energie_totale = 0
        # Initialiser les dictionnaires pour stocker les résultats par canal
        self.energie_par_canal = {}
        self.photons_par_canal = {}
        
        # Initialisation des dictionnaires avec les canaux spectraux
        for canal in self.plage_lambda.keys():
            self.energie_par_canal[canal] = 0
            self.photons_par_canal[canal] = 0
        
        for _, row in self.data.iterrows():
            # Étape 2: Récupérer les valeurs d'éclairement par canal (lux)
            for canal in self.plage_lambda.keys():
                # Valeur d'éclairement direct pour ce canal (lux)
                canal_lux = row[canal]
                
                # Conversion en puissance avec facteur spécifique au canal
                densite_puissance = canal_lux * self.lux_en_wat_selon_spectre[canal]  # W/m²
                puissance = densite_puissance * self.surface  # Watts 
                
                # Paramètres du canal
                min_nm, max_nm = self.plage_lambda[canal]
                moyenne_lambda = (min_nm + max_nm) / 2
                
                # Énergie d'un photon à cette longueur d'onde
                energie_photon = self.calculer_energie_photon(moyenne_lambda)  # Joules
                
                # Nombre de photons par seconde dans ce canal
                photons_par_sec = puissance / energie_photon if energie_photon > 0 else 0
                
                # Énergie et photons sur l'intervalle delta_t
                canal_energie = puissance * self.delta_t  # Joules
                photons = photons_par_sec * self.delta_t
                
                # Accumulation
                self.energie_par_canal[canal] += canal_energie
                self.photons_par_canal[canal] += photons
                self.energie_totale += canal_energie

    def formater_resultats_texte(self):
        # Affiche les résultats des calculs
        print(f"Énergie totale absorbée sur 24h: {self.energie_totale/1000:.1f} kJoules")

        print("\nÉnergie par canal spectral:")
        max_len = max(len(canal) for canal in self.energie_par_canal.keys())
        for canal, energy in self.energie_par_canal.items():
            min_nm, max_nm = self.plage_lambda[canal]
            label = f"{canal} ({min_nm}-{max_nm} nm)".ljust(max_len + 20)
            print(f"{label}: {energy:.2f} J ({energy/self.energie_totale*100:.1f}%)")

        print("\nNombre de photons par canal spectral:")
        for canal, photons in self.photons_par_canal.items():
            min_nm, max_nm = self.plage_lambda[canal]
            label = f"{canal} ({min_nm}-{max_nm} nm)".ljust(max_len + 20)
            print(f"{label}: {photons:.2e} photons")

        print("\n")

    def get_resultats_energie(self):
        self.calculer_energie()

        # Retourne les résultats sous forme de dictionnaire
        resultats = {
            'energie_totale': self.energie_totale,
            'energie_par_canal': self.energie_par_canal,
            'photons_par_canal': self.photons_par_canal,
            'unite_convertion': self.unite_convertion
        }
        return resultats

    def afficher_graphique_resultats(self, ax=None, fig=None):
        # Préparation des données
        canaux = list(self.plage_lambda.keys())

        # Conversion des joules selon la superficie
        self.unite_convertion = 'J'
        if self.surface < 50 : # en kilojoules
            energies_xj = [self.energie_par_canal[canal] / 1e3 for canal in canaux]
            self.unite_convertion = 'kJ'
        elif self.surface >= 50 and self.surface <= 2500 : # en mega-joules 
            energies_xj = [self.energie_par_canal[canal] / 1e6 for canal in canaux]
            self.unite_convertion = 'MJ'
        elif self.surface > 2500 and self.surface < 50000: # en giga-joules
            energies_xj = [self.energie_par_canal[canal] / 1e9 for canal in canaux]
            self.unite_convertion = 'GJ'
        else: # en tera-joules
            energies_xj = [self.energie_par_canal[canal] / 1e12 for canal in canaux]
            self.unite_convertion = 'TJ'

        # Labels avec juste la longueur d'onde
        labels_propres = [canal[-5:-2] for canal in canaux]
        
        # Couleurs correspondant approximativement aux longueurs d'onde
        couleurs = {
            'Violet_415nm': '#8A2BE2',  # Violet
            'Indigo_445nm': '#4B0082',  # Indigo
            'Bleu_480nm': '#0000FF',    # Bleu
            'Cyan_515nm': '#00FFFF',    # Cyan
            'Vert_555nm': '#00FF00',    # Vert
            'Jaune_590nm': '#FFFF00',   # Jaune
            'Orange_630nm': '#FFA500',  # Orange
            'Rouge_680nm': '#FF0000'    # Rouge
        }
        
        # Liste des couleurs pour les barres
        liste_couleurs = [couleurs[canal] for canal in canaux]
        
        # Graphique des énergies par canal spectral
        # Créer un axe si aucun n'est fourni
        if ax is None:
            fig, ax = plt.subplots(figsize=(11, 6))

        bars = plt.bar(labels_propres, energies_xj, color=liste_couleurs)
        bars = ax.bar(labels_propres, energies_xj, color=liste_couleurs)

        plt.title('Énergie par canal spectral')
        plt.ylabel(f'Énergie ({self.unite_convertion})')
        plt.xlabel('Canal spectral (nm)')
        ax.set_facecolor('#fffcfc') 
        fig.set_facecolor('#fffcfc') 
        
        # Ajout des valeurs numériques au-dessus des barres
        for bar, energy in zip(bars, energies_xj):
            height = bar.get_height()
            plt.text(bar.get_x() + bar.get_width()/2., height + height*0.05,
                    f'{energy:.1f} {self.unite_convertion} ', ha='center', va='bottom', fontsize=9)

        # Affichage uniquement si ax est None (à revoir)
        if ax is None:
            plt.tight_layout()
            plt.show()

'''
""" Exemple d'utilisation """
# energie_plante = Energie(0.01)
# energie_plante.afficher_graphique_resultats()
# energie_plante.formater_resultats_texte() # Si besoin de lire les résultats dans la console

    # def formater_resultats_texte(self):
    #     # Affiche les résultats des calculs
    #     print(f"Énergie totale absorbée sur 24h: {self.energie_totale/1000:.1f} kJoules")
    #     print("\nÉnergie par canal spectral:")
    #     for canal, energy in self.energie_par_canal.items():
    #         min_nm, max_nm = self.plage_lambda[canal]
    #         print(f"{canal} ({min_nm}-{max_nm} nm): {energy:.2f} J ({energy/self.energie_totale*100:.1f}%)")
        
    #     print("\nNombre de photons par canal spectral:")
    #     for canal, photons in self.photons_par_canal.items():
    #         min_nm, max_nm = self.plage_lambda[canal]
    #         print(f"{canal} ({min_nm}-{max_nm} nm): {photons:.2e} photons")
'''