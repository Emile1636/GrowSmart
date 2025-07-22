#derivee
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from load_fichier_csv import load_data_from_gist
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from tkinter import ttk, font
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure


class Derivee():

    def __init__(self, plante):
        self.plante = plante

    def calculs(self, plante):
        data = load_data_from_gist()

        data['Date'] = pd.to_datetime(data['Date'])
        journée = data['Date'].dt.strftime("%Y-%m-%d")

######################################## parcourir le fichier csv avant et si donnée aberrante, changer la donnée pour la moyenne avec la donnée avant et la donnée après
    ###### pour l'humidité du sol aussi!!!!

        for i in range(len(data)):       
            if data.loc[i,'Humidité ambiante'] == -1 or pd.isna(data.loc[i, 'Humidité ambiante']) or data.loc[i, 'Température'] == -1 or pd.isna(data.loc[i, 'Température']) or data.loc[i, plante] == -1 or pd.isna(data.loc[i, plante]):
                if 0 < i < len(data) - 1: 
                    data.loc[i, 'Humidité ambiante'] = (data.loc[i-1, 'Humidité ambiante']+data.loc[i+1, 'Humidité ambiante'])/2
                    data.loc[i, plante] = (data.loc[i-1, plante]+data.loc[i+1, plante])/2

                    if abs(data.loc[i, 'Température'] - data.loc[i-1, 'Température']) > 10 and abs(data.loc[i+1, 'Température'] - data.loc[i, 'Température']) > 10 :
                        data.loc[i, 'Température'] = (data.loc[i-1, 'Température'] + data.loc[i+1, 'Température'])/2
                elif i == len(data)-1:
                    data.loc[i, 'Humidité ambiante'] = data.loc[i-1,'Humidité ambiante']
                    data.loc[i, plante] = data.loc[i-1, plante]
                    if abs(data.loc[i, 'Température'] - data.loc[i-1, 'Température']) > 10:
                        data.loc[i, 'Température'] = data.loc[i-1, 'Température']
                elif i == 0:
                    data.loc[i, 'Humidité ambiante'] = data.loc[i+1, 'Humidité ambiante']
                    data.loc[i, plante] = data.loc[i+1, plante]
                    if abs(data.loc[i+1, 'Température'] - data.loc[i, 'Température']) > 10:
                        data.loc[i, 'Température'] = data.loc[i+1, 'Température']

            

        #attribution des valeurs des variables
        x = data['Date'].dt.strftime("%H:%M")
        y1 = data[plante]
        y2 = data['Humidité ambiante']
        y3 = data['Température']
        y4 = data['Clear']

    
        ###calculs de dérivée###
        ##conversions
        xf = pd.to_datetime(x, format="%H:%M").dt.time
        x_base_10 = np.array([t.hour + t.minute / 60 for t in xf], dtype=float)
        for i in range(len(data)):
            if x_base_10[i-1] > x_base_10[i]:
                for k in range(i, 95):
                    x_base_10[k] = x_base_10[k]+24
        if x_base_10[k] == x_base_10[0]:
            for j in range(k, 95):
                x_base_10[j] = x_base_10[j]-24
                    
            
        #Calculs de dérivées
        y1_f = np.array(y1, dtype=float)
        y2_f = np.array(y2, dtype=float)
        y3_f = np.array(y3, dtype=float)
        y4_f = np.array(y4, dtype=float)

        ###erreur division par zéro
        try:
            dy1_dx = np.gradient(y1_f, x_base_10)
            dy2_dx = np.gradient(y2_f, x_base_10)
            dy3_dx = np.gradient(y3_f, x_base_10)
            dy4_dx = np.gradient(y4_f, x_base_10)
        except ZeroDivisionError:
            print("ERREUR : Division par zéro dans le calcul de la dérivée")


        #dérivées min, max, moy
        min_deriv1 = np.min(dy1_dx)
        max_deriv1 = np.max(dy1_dx)
        moy_deriv1 = np.mean(dy1_dx)

        min_deriv2 = np.min(dy2_dx)
        max_deriv2 = np.max(dy2_dx)
        moy_deriv2 = np.mean(dy2_dx)

        min_deriv3 = np.min(dy3_dx)
        max_deriv3 = np.max(dy3_dx)
        moy_deriv3 = np.mean(dy3_dx)

        min_deriv4 = np.min(dy4_dx)
        max_deriv4 = np.max(dy4_dx)
        moy_deriv4 = np.mean(dy4_dx)


        #données min, max, moy
        min_donnee1 = np.min(y1_f)
        max_donnee1 = np.max(y1_f)
        moy_donnee1 = np.mean(y1_f)

        min_donnee2 = np.min(y2_f)
        max_donnee2 = np.max(y2_f)
        moy_donnee2 = np.mean(y2_f)

        min_donnee3 = np.min(y3_f)
        max_donnee3 = np.max(y3_f)
        moy_donnee3 = np.mean(y3_f)

        min_donnee4 = np.min(y4_f)
        max_donnee4 = np.max(y4_f)
        moy_donnee4 = np.mean(y4_f)


   
        #ajouter dans tableau
        tableau_données = pd.DataFrame({
        "Types de données": ["Dérivées minimales", "Dérivées maximales", "Dérivées moyennes", "Valeurs minimales", "Valeurs maximales", "Valeurs moyennes"], 
        f"Humidité du sol (%) {plante}": [min_deriv1, max_deriv1, moy_deriv1, min_donnee1, max_donnee1, moy_donnee1],
        "Humidité ambiante (%)": [min_deriv2, max_deriv2, moy_deriv2, min_donnee2, max_donnee2, moy_donnee2],
        "Température (°C)": [min_deriv3, max_deriv3, moy_deriv3, min_donnee3, max_donnee3, moy_donnee3],
        "Luminosité (lux)" : [min_deriv4, max_deriv4, moy_deriv4, min_donnee4, max_donnee4, moy_donnee4]
        })
    

        return x, y1, y2, y3, y4, journée, x_base_10, dy1_dx, dy2_dx, dy3_dx, dy4_dx, tableau_données


    #les graphiques

    def graphique1_les_humidites(self, plante):
        x, y1, y2, y3, y4, journée, x_base_10, dy1_dx, dy2_dx, dy3_dx, dy4_dx, tableau_données = self.calculs(plante)
        #création du graphique1(tout sauf la luminosité et température)
        fig = Figure(figsize=(10, 6))
        ax = fig.add_subplot(111)
        ax.plot(x, y1, "o", linestyle='-', color='blue', linewidth=3, label="Humidité du sol (%)", markersize=1)
        ax.plot(x, y2, "o", linestyle='-', color='orange', linewidth=3, label="Humidité ambiante (%)", markersize=1)
        ax.set_xlabel(f'Temps (heures) \n À partir de {journée[0]} à {journée[95]}')
        ax.set_ylabel('Paramètres de la plante')
        ax.set_title(f"Statistiques de la plante {plante}")
        ax.set_xticks([x[0], x[11], x[23], x[35], x[47], x[59], x[71], x[83], x[95]])
        ax.legend(bbox_to_anchor=(0.2, 1.13))
        ax.grid()
        ax.set_facecolor('#fffcfc') 
        fig.set_facecolor('#fffcfc') 
        return fig


    def graphique2_temperature(self, plante):
        x, y1, y2, y3, y4, journée, x_base_10, dy1_dx, dy2_dx, dy3_dx, dy4_dx, tableau_données = self.calculs(plante)
        #création du graphique2(température)
        fig = Figure(figsize=(10, 6))
        ax = fig.add_subplot(111)
        ax.plot(x, y3, "o", linestyle='-', color='green', linewidth=3, label="Température (°C)", markersize=1)
        ax.set_xlabel(f'Temps (heures) \n À partir de {journée[0]} à {journée[95]}')
        ax.set_ylabel('Paramètres de la plante')
        ax.set_title(f"Statistiques de la température de la plante {plante}")
        ax.set_xticks([x[0], x[11], x[23], x[35], x[47], x[59], x[71], x[83], x[95]])
        ax.legend(bbox_to_anchor=(0.2, 1.13))
        ax.grid()
        ax.set_facecolor('#fffcfc') 
        fig.set_facecolor('#fffcfc') 
        return fig


    def graphique3_luminosite(self, plante):
        x, y1, y2, y3, y4, journée, x_base_10, dy1_dx, dy2_dx, dy3_dx, dy4_dx, tableau_données = self.calculs(plante)
        #création du graphique3(luminosité)
        fig = Figure(figsize=(10, 6))
        ax = fig.add_subplot(111)
        ax.plot(x, y4, "o", linestyle='-', color='red', linewidth=3, label="Luminosité (lux)", markersize=1)
        ax.set_xlabel(f'Temps (heures) \n À partir de {journée[0]} à {journée[95]}')
        ax.set_ylabel('Paramètres de la plante')
        ax.set_title(f"Statistiques (luminosité) de la plante {plante}")
        ax.set_xticks([x[0], x[11], x[23], x[35], x[47], x[59], x[71], x[83], x[95]])
        ax.legend(bbox_to_anchor=(0.2, 1.13))
        ax.grid()
        ax.set_facecolor('#fffcfc') 
        fig.set_facecolor('#fffcfc') 
        return fig


    def graphique4_derivee_humidite_sol(self, plante):
        x, y1, y2, y3, y4, journée, x_base_10, dy1_dx, dy2_dx, dy3_dx, dy4_dx, tableau_données = self.calculs(plante)
        ##dérivée Capteur Humidité du sol
        fig = Figure(figsize=(10, 6))
        ax = fig.add_subplot(111)
        ax.plot(x_base_10[1:-1], dy1_dx[1:-1], "o", linestyle='-', color='blue', linewidth=3, label="VARIATION de l'humidité du sol (%)", markersize=3)
        ax.set_title(f'La variation de humidité du sol en fonction du temps pour la plante {plante}')
        ax.set_xlabel(f'Temps (heures) \n À partir de {journée[0]}  {x[0]}   à   {journée[95]}  {x[95]}')
        ax.set_ylabel('Dérivée')
        ax.legend(bbox_to_anchor=(0.2, 1.13))
        ax.grid()
        ax.set_facecolor('#fffcfc') 
        fig.set_facecolor('#fffcfc') 
        return fig
        

    def graphique5_derivee_humidite_ambiante(self, plante):
        x, y1, y2, y3, y4, journée, x_base_10, dy1_dx, dy2_dx, dy3_dx, dy4_dx, tableau_données = self.calculs(plante)
        ##dérivée Capteur Humidité ambiante
        fig = Figure(figsize=(10, 6))
        ax = fig.add_subplot(111)
        ax.plot(x_base_10[1:-1], dy2_dx[1:-1], "o", linestyle='-', color='orange', linewidth=3, label="VARIATION de l'humidité ambiante (%)", markersize=3)
        ax.set_title(f'La variation de humidité ambiante en fonction du temps pour la plante {plante}')
        ax.set_xlabel(f'Temps (heures) \n À partir de {journée[0]}  {x[0]}   à   {journée[95]}  {x[95]}')
        ax.set_ylabel('Dérivée')
        ax.legend(bbox_to_anchor=(0.2, 1.13))
        ax.grid()
        ax.set_facecolor('#fffcfc') 
        fig.set_facecolor('#fffcfc') 
        return fig

    def graphique6_derivee_temperature(self, plante):
        x, y1, y2, y3, y4, journée, x_base_10, dy1_dx, dy2_dx, dy3_dx, dy4_dx, tableau_données = self.calculs(plante)
        ##dérivée Capteur Température
        fig = Figure(figsize=(10, 6))
        ax = fig.add_subplot(111)
        ax.plot(x_base_10[1:-1], dy3_dx[1:-1], "o", linestyle='-', color='green', linewidth=3, label="VARIATION de la température (°C)", markersize=3)
        ax.set_title(f'La variation de température en fonction du temps pour la plante {plante}')
        ax.set_xlabel(f'Temps (heures) \n À partir de {journée[0]}  {x[0]}   à   {journée[95]}  {x[95]}')
        ax.set_ylabel('Dérivée')
        ax.legend(bbox_to_anchor=(0.2, 1.13))
        ax.grid()
        ax.set_facecolor('#fffcfc') 
        fig.set_facecolor('#fffcfc') 
        return fig
        

    def graphique7_derivee_luminosite(self, plante):
        x, y1, y2, y3, y4, journée, x_base_10, dy1_dx, dy2_dx, dy3_dx, dy4_dx, tableau_données = self.calculs(plante)
        ##dérivée Capteur luminosité
        fig = Figure(figsize=(10, 6))
        ax = fig.add_subplot(111)
        ax.plot(x_base_10[1:-1], dy4_dx[1:-1], "o", linestyle='-', color='red', linewidth=3, label="VARIATION de la luminosité (lux)", markersize=3)
        ax.set_title(f'La variation de luminosité en fonction du temps pour la plante {plante}')
        ax.set_xlabel(f'Temps (heures) \n À partir de {journée[0]}  {x[0]}   à   {journée[95]}  {x[95]}')
        ax.set_ylabel('Dérivée')
        ax.legend(bbox_to_anchor=(0.2, 1.13))
        ax.grid()
        ax.set_facecolor('#fffcfc') 
        fig.set_facecolor('#fffcfc') 
        return fig
        

    def tableau_resume(self, frame, plante):
        x, y1, y2, y3, y4, journée, x_base_10, dy1_dx, dy2_dx, dy3_dx, dy4_dx, tableau_données = self.calculs(plante)
        tableau_données = tableau_données.round(2)
        # Supprimer les widgets éventuels
        for widget in frame.winfo_children():
            widget.destroy()

        #Style d'écriture
        style = ttk.Style()
        style.configure("Treeview", font=("Arial", 15))
        style.configure("Treeview.Heading", foreground="green", font=("Arial", 17, "bold"))

        # Créer le Treeview dans le nouveau frame
        tree = ttk.Treeview(frame, columns=list(tableau_données.columns), show="headings")
        tree.pack(fill="both", expand=True)

        #taille du frame
        frame.configure(width=1500, height=250)
        frame.pack_propagate(False)

        for col in tableau_données.columns:
            tree.heading(col, text=col)
            tree.column(col, anchor="center")

        for i, row in tableau_données.iterrows():
            tree.insert("", "end", values=[""] * len(tableau_données.columns))
            tree.insert("", "end", values=list(row))


        return tableau_données


