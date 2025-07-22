# graph.py : implémentation scientifique

"""

Contextes :
    Éléments récupérés dans le fichier CSV (96 prises de données, une au 15min pendant 24h):
        - Date de la prise de données
        - Humidité du sol : Capteur 1, Capteur 2, Capteur 3, Capteur 4, Capteur 5
        - Humidité ambiante
        - Température ambiante
        - Intensité lumineuse totale : Clear
        - Intensité selon les spectres : Violet, Indigo, Bleu, Cyan, Vert, Jaune, Orange, Rouge
    Dans le format suivant lorsque load_data_from_gist est appelé : 
        column_names = [
                'Date', 
                'Capteur 1', 'Capteur 2', 'Capteur 3', 'Capteur 4', 'Capteur 5', 
                'Humidité ambiante', 'Température',
                'Violet_415nm', 'Indigo_445nm', 'Bleu_480nm', 'Cyan_515nm',
                'Vert_555nm', 'Jaune_590nm', 'Orange_630nm', 'Rouge_680nm',
                'Clear', 'NIR'
        ]

Graph :
    Type de relation entre les données : 
        - Noeuds : Capteurs 1 à 5
        - Liens : 1 - Indice de corrélation entres deux valeurs 
                  2 - Probabilité de changé d'état? (Lien à faire avec les prédictions) # Ne pas faire pour l'instant
    Sujets des graphs :
        1 - "Impact des conditions ambiantes sur l'humidité du sol"

Objectif : Définir les relations entre les capteurs et les données. Afficher les relations sous forme de graphes.

"""

import networkx as nx
import sys
import os
import matplotlib.pyplot as plt

import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from load_fichier_csv import load_data_from_gist 

class Graph:
    def __init__(self):
        self.data = self.charger_donnees()
        self.setup_graph()
        
    def charger_donnees(self):
        return load_data_from_gist()
    
    def setup_graph(self):
        self.G = nx.Graph()
        self.create_nodes()

    def create_nodes(self):
        # Regrouper les noeuds
        self.soil_sensors = ['Capteur 1', 'Capteur 2', 'Capteur 3', 'Capteur 4', 'Capteur 5']
        self.ambient = ['Humidité ambiante', 'Température']
        self.light_spectrum = ['Violet_415nm', 'Indigo_445nm', 'Bleu_480nm', 'Cyan_515nm','Vert_555nm', 'Jaune_590nm', 'Orange_630nm', 'Rouge_680nm','Clear', 'NIR']
        
        # Ajout des noeuds selon leur catégorie
        for sensor in self.soil_sensors:
            self.G.add_node(sensor, category='sol')
            
        for ambient in self.ambient:
            self.G.add_node(ambient, category='ambiant')
            
        for spectrum in self.light_spectrum:
            self.G.add_node(spectrum, category='lumière')
        
    def get_correlation_matrix(self):
        # Calcule la matrice de corrélation de Pearson entre toutes les variables
        colonnes_numeriques = self.soil_sensors + self.ambient + self.light_spectrum
        df_numerique = self.data[colonnes_numeriques]
        correlation_matrix = df_numerique.corr(method='spearman') # spearman pearson
        return correlation_matrix
        
    def cree_graph_sujet_1(self): # Impact des conditions ambiantes sur l'humidité du sol
        # On réinitialise le graphe pour ce sujet spécifique
        self.G = nx.Graph()
        
        # On ajoute les noeuds d'humidité du sol et les conditions ambiantes + lumière
        noeuds_ambiance = self.ambient + ['Clear']
        
        # Ajouter les noeuds
        for sensor in self.soil_sensors:
            self.G.add_node(sensor, category='sol')
        
        for condition in noeuds_ambiance:
            self.G.add_node(condition, category='ambiant')
        
        # Calculer la matrice de corrélation
        corr_matrix = self.get_correlation_matrix()
        
        # Ajouter les liens entre les capteurs d'humidité et les conditions ambiantes
        for sensor in self.soil_sensors:
            for condition in noeuds_ambiance:
                correlation = corr_matrix.loc[sensor, condition]
                self.G.add_edge(sensor, condition, weight=correlation, correlation=round(correlation, 2))
        
        return self.G

    def creer_figure_graph(self, title="Graphe de corrélation"): # Crée et retourne une figure matplotlib avec le graphe, sans l'afficher
        fig = plt.figure(figsize=(5, 4), facecolor='#fffcfc')
        ax = fig.add_subplot(111, facecolor='#fffcfc')
        
        # Renommer les nœuds spécifiques avant de créer le graphe
        mapping = {
            'Humidité ambiante': 'Humidité',
            'Clear': 'Lumière'
        }
        
        # Appliquer le renommage au graphe
        self.G = nx.relabel_nodes(self.G, mapping)
        
        # Définir des positions fixes pour les nœuds selon leur catégorie
        pos = {}
        
        # Placer les capteurs de sol en ligne verticale à gauche
        soil_sensors = [node for node in self.G.nodes() if self.G.nodes[node]['category'] == 'sol']
        soil_count = len(soil_sensors)
        for i, sensor in enumerate(soil_sensors):
            pos[sensor] = (0.2, 0.9 - (i * 0.8 / (soil_count - 1 if soil_count > 1 else 1)))
        
        # Placer les conditions ambiantes en ligne verticale à droite
        ambient_sensors = [node for node in self.G.nodes() if self.G.nodes[node]['category'] == 'ambiant']
        ambient_count = len(ambient_sensors)
        for i, sensor in enumerate(ambient_sensors):
            pos[sensor] = (0.8, 0.9 - (i * 0.8 / (ambient_count - 1 if ambient_count > 1 else 1)))
        
        # Si d'autres types de nœuds sont présents, les placer au milieu
        other_sensors = [node for node in self.G.nodes() if self.G.nodes[node]['category'] not in ['sol', 'ambiant']]
        other_count = len(other_sensors)
        for i, sensor in enumerate(other_sensors):
            pos[sensor] = (0.5, 0.9 - (i * 0.8 / (other_count - 1 if other_count > 1 else 1)))
        
        # Récupération des poids des arêtes pour l'épaisseur et la couleur
        # Ajuster l'échelle pour que l'épaisseur varie de 1 à 10 selon la force de la corrélation
        edge_weights = []
        edge_colors = []
        
        for u, v in self.G.edges():
            # Valeur absolue pour l'épaisseur (la force de la corrélation indépendamment du signe)
            abs_corr = abs(self.G[u][v]['weight'])
            # Appliquer une échelle non linéaire pour mieux différencier les corrélations
            # Multiplier par x pour avoir des traits très épais pour les fortes corrélations
            edge_weights.append(1 + abs_corr * 10)
            # Valeur réelle (avec signe) pour la couleur
            edge_colors.append(self.G[u][v]['weight'])
        
        # Couleurs des nœuds selon catégorie
        node_colors = []
        for node in self.G.nodes():
            category = self.G.nodes[node]['category']
            if category == 'sol':
                node_colors.append('skyblue')
            elif category == 'ambiant':
                node_colors.append('orange')
            else:  # lumière
                node_colors.append('green')
        
        # Dessiner les nœuds
        nx.draw_networkx_nodes(self.G, pos, node_color=node_colors, node_size=500, ax=ax)
        
        # Dessiner les arêtes avec l'épaisseur variable
        edges = nx.draw_networkx_edges(self.G, pos, width=edge_weights, edge_color=edge_colors, edge_cmap=plt.cm.RdBu, edge_vmin=-1.0, edge_vmax=1.0, ax=ax)
        
        # Dessiner les labels des nœuds
        nx.draw_networkx_labels(self.G, pos, font_size=8, ax=ax)
        
        # Ajouter une légende pour les couleurs des nœuds et l'épaisseur des arêtes
        from matplotlib.lines import Line2D
        
        # Légende pour les types de nœuds
        node_legend_elements = [
            Line2D([0], [0], marker='o', color='w', markerfacecolor='skyblue', markersize=10, label='Capteurs sol'),
            Line2D([0], [0], marker='o', color='w', markerfacecolor='orange', markersize=10, label='Conditions ambiantes')
        ]
        if any(self.G.nodes[node]['category'] not in ['sol', 'ambiant'] for node in self.G.nodes()):
            node_legend_elements.append(
                Line2D([0], [0], marker='o', color='w', markerfacecolor='green', markersize=10, label='Spectre lumineux')
            )
        
        # Légende pour l'épaisseur des arêtes (corrélation)
        edge_legend_elements = [
            Line2D([0], [0], color='lightgray', lw=5, label='Faible corrélation'),
            Line2D([0], [0], color='gray', lw=8, label='Forte corrélation')
        ]
        
        # Placer deux légendes distinctes
        ax.legend(handles=node_legend_elements, loc='upper center', bbox_to_anchor=(0.5, -0.05), ncol=3, fontsize=8)
        ax.add_artist(plt.legend(handles=edge_legend_elements, loc='lower center', bbox_to_anchor=(0.5, -0.2), ncol=2, fontsize=8))
        
        # Titre
        ax.set_title(title, fontsize=14)
        ax.axis('off')
        
        # Ajuster les marges pour accommoder les légendes
        fig.tight_layout(rect=[0, 0.1, 1, 0.95])
        fig.patch.set_facecolor('#fffcfc')  # Couleur de fond de la figure entière

        # Téléchargement de la figure
        # plt.savefig('graph.png', dpi=300, bbox_inches='tight')
        
        return fig
    
    def get_info_capteur(self, no):
        # Récupérer les informations du capteur
        no_capteur = 'Capteur ' + str(no)
        if no_capteur in self.G.nodes:
            # Récupérer l'élément entre la température, l'humidité ambiante ou la luminosité qui influence le plus ce capteur
            # Valeur absolue de la force de la corrélation
            correlations = {k: abs(v['weight']) for k, v in self.G[no_capteur].items()}
            # Trier 
            sorted_correlations = sorted(correlations.items(), key=lambda x: x[1], reverse=True)
            if sorted_correlations:
                influence_sensor, _ = sorted_correlations[0]
                correlation_value = self.G[no_capteur][influence_sensor]['weight'] # Valeur
                sensor_type = self.G.nodes[influence_sensor]['category'] # Type
                
                resultats = {
                    'Capteur': no_capteur,
                    'Influence': influence_sensor,
                    'Type': sensor_type,
                    'Corrélation': round(correlation_value, 2)
                }
                return resultats
        else:
            return -1
        
# Exemple d'utilisation
if __name__ == "__main__":
    ...
    # graph = Graph()
    # Graphe du sujet 1: Impact des conditions ambiantes sur l'humidité du sol
    # graph.cree_graph_sujet_1()
    # graph.creer_figure_graph(title="Impact des conditions ambiantes sur l'humidité du sol")
    # plt.show()
    # graph.afficher_graph(title="Impact des conditions ambiantes sur l'humidité du sol")

# Code supplémentaire, facultatif.
"""  
# Graphe du sujet 2: Relations entre capteurs d'humidité du sol

    def cree_graph_sujet_2(self): # Relations entre capteurs d'humidité du sol
        # On réinitialise le graphe pour ce sujet spécifique
        self.G = nx.Graph()
        
        # Ajouter seulement les capteurs d'humidité du sol
        for sensor in self.soil_sensors:
            self.G.add_node(sensor, category='sol')
        
        # Calculer la matrice de corrélation
        corr_matrix = self.get_correlation_matrix()
        
        # Ajouter les liens entre les capteurs d'humidité du sol
        for i, sensor1 in enumerate(self.soil_sensors):
            for sensor2 in self.soil_sensors[i+1:]:  # Éviter les doublons
                correlation = corr_matrix.loc[sensor1, sensor2]
                # On garde toutes les corrélations pour voir les relations entre capteurs
                self.G.add_edge(sensor1, sensor2, weight=correlation, correlation=round(correlation, 2))
        
        return self.G

    # Graphe du sujet 2: Relations entre capteurs d'humidité du sol
    graph.cree_graph_sujet_2()
    graph.afficher_graph(title="Relations entre capteurs d'humidité du sol")

 """
