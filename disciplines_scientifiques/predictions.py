#predictions

import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from load_fichier_csv import load_data_from_gist
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import customtkinter as ctk
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# data = load_data_from_gist()
# plante = "Capteur 1"
# x1 = np.array(data['Humidité ambiante'], dtype=float)
# x2 = np.array(data['Température'], dtype=float)
# x3 = np.array(data['Clear'], dtype=float)
# y = data[plante]

class Predictions:

    def __init__(self, data=None, plante=None):
        self.data = load_data_from_gist()
        self.plante = data[plante]
        self.humidite_du_sol(data, plante)
        self.humidite_ambiante(data, plante)
        self.temperature(data, plante)
        np.seterr(invalid='ignore')

    def humidite_du_sol(self, data, plante_n):

        # print(data)
        plante=(f"Capteur {plante_n}")
        # print (plante)
        data['Date'] = pd.to_datetime(data['Date'])
        x = data['Date'].dt.strftime("%H:%M")
        xf = pd.to_datetime(x, format="%H:%M").dt.time
        x_base_10 = np.array([t.hour + t.minute / 60 for t in xf], dtype=float)
        for i in range(len(data)):
            if x_base_10[i-1] > x_base_10[i]:
                for k in range(i, 95):
                    x_base_10[k] = x_base_10[k]+24
        if x_base_10[k] == x_base_10[0]:
            for j in range(k, 95):
                x_base_10[j] = x_base_10[j]-24

        x1 = np.array(data['Humidité ambiante'], dtype=float)
        x2 = np.array(data['Température'], dtype=float)
        x3 = np.array(data['Clear'], dtype=float)
        y = np.array(data[plante], dtype=float)

        #ajout de précision des résultats en prenant seulement les dernières valeurs
        x_base_10 = x_base_10[88:]
        x1 = x1[88:]
        x2 = x2[88:]
        x3 = x3[88:]
        y = y[88:]

        
        ponderation = [1, 2, 3, 4, 7, 8, 9, 10, 11]

        #calculs dérivées
        try:
            dy_dx1 = np.gradient(y, x1)
            dy_dx2 = np.gradient(y, x2)
            dy_dx3 = np.gradient(y, x3)
            dy_dx4 = np.gradient(y, x_base_10)
        except ZeroDivisionError:
            print("ERREUR : Division par zéro dans le calcul de la dérivée")
       
        dy_dx1_clean = np.where(np.isfinite(dy_dx1),dy_dx1,0)
        dy_dx2_clean = np.where(np.isfinite(dy_dx2),dy_dx2,0)
        dy_dx3_clean = np.where(np.isfinite(dy_dx3),dy_dx3,0)
        dy_dx4_clean = np.where(np.isfinite(dy_dx4),dy_dx4,0)
        

        # print(dy_dx1_clean, dy_dx2_clean, dy_dx3_clean, dy_dx4_clean)

        moy_deriv1 = 0
        for x, y in zip(dy_dx1_clean, ponderation):
            moy_deriv1 += x * y
        average1 = moy_deriv1 / sum(ponderation)
        # print("{:.4f}".format(average1))
        moy_deriv2 = 0
        for x, y in zip(dy_dx2_clean, ponderation):
            moy_deriv2 += x * y
        average2 = moy_deriv2 / sum(ponderation)
        # print("{:.4f}".format(average2))
        moy_deriv3 = 0
        for x, y in zip(dy_dx3_clean, ponderation):
            moy_deriv3 += x * y
        average3 = moy_deriv3 / sum(ponderation)
        # print("{:.4f}".format(average3))
        moy_deriv4 = 0
        for x, y in zip(dy_dx4_clean, ponderation):
            moy_deriv4 += x * y
        average4 = moy_deriv4 / sum(ponderation)
        # print("{:.4f}".format(average4))

        # print("{:.4f}".format(moy_deriv1), "{:.4f}".format(moy_deriv2), "{:.4f}".format(moy_deriv3), "{:.4f}".format(moy_deriv4))


        impact_direct = [moy_deriv1, moy_deriv4]
        impact_inverse = [moy_deriv2, moy_deriv3]
        augmente = 0
        diminue = 0
        neutre = 0

        #résultats
        #humidité ambiant et temps impact direct
        for i in impact_direct:
            if i > 0 :
                augmente += 1
            elif i < 0 :
                diminue += 1
            elif i == 0 :
                neutre += 1

        #impact inverse de la température et de la luminosité
        for i in impact_inverse:
            if i < 0 :
                augmente += 1
            elif i > 0 :
                diminue += 1
            elif i == 0 :
                neutre += 1

        probabilités_augmente = (augmente/4)*100
        probabilités_diminue = (diminue/4)*100
        probabilités_neutre = (neutre/4)*100

        # print("Il y a ", "{:.2f}".format(probabilités_augmente)," % que l'humidité du sol augmente.")
        # print(f"Il y a ", "{:.2f}".format(probabilités_diminue)," % que l'humidité du sol diminue.")
        # print(f"Il y a ", "{:.2f}".format(probabilités_neutre)," % que l'humidité du sol ne varie pas.")

        var=[probabilités_augmente,probabilités_diminue,probabilités_neutre]
        return var #renvoi les données




    def humidite_ambiante(self, data, plante_n):
        plante=(f"Capteur {plante_n}")
        # print (plante)
        data['Date'] = pd.to_datetime(data['Date'])
        x = data['Date'].dt.strftime("%H:%M")
        xf = pd.to_datetime(x, format="%H:%M").dt.time
        x_base_10 = np.array([t.hour + t.minute / 60 for t in xf], dtype=float)
        for i in range(len(data)):
            if x_base_10[i-1] > x_base_10[i]:
                for k in range(i, 95):
                    x_base_10[k] = x_base_10[k]+24
        if x_base_10[k] == x_base_10[0]:
            for j in range(k, 95):
                x_base_10[j] = x_base_10[j]-24

        x1 = np.array(data['Température'], dtype=float)
        x2 = np.array(data['Clear'], dtype=float)
        y = np.array(data[plante], dtype=float)

        #ajout de précision des résultats en prenant seulement les dernières valeurs
        x_base_10 = x_base_10[88:]
        x1 = x1[88:]
        x2 = x2[88:]
        y = y[88:]

        ponderation = [1, 2, 3, 4, 7, 8, 9, 10, 11]

        #calculs dérivées
        try:
            dy_dx1 = np.gradient(y, x1)
            dy_dx2 = np.gradient(y, x2)
            dy_dx3 = np.gradient(y, x_base_10)
        except ZeroDivisionError:
            print("ERREUR : Division par zéro dans le calcul de la dérivée")

        dy_dx1_clean = np.where(np.isfinite(dy_dx1),dy_dx1,0)
        dy_dx2_clean = np.where(np.isfinite(dy_dx2),dy_dx2,0)
        dy_dx3_clean = np.where(np.isfinite(dy_dx3),dy_dx3,0)


        # print(dy_dx1_clean, dy_dx2_clean, dy_dx3_clean)

        moy_deriv1 = 0
        for x, y in zip(dy_dx1_clean, ponderation):
            moy_deriv1 += x * y

        average1 = moy_deriv1 / sum(ponderation)
        # print("{:.4f}".format(average1))

        moy_deriv2 = 0
        for x, y in zip(dy_dx2_clean, ponderation):
            moy_deriv2 += x * y

        average2 = moy_deriv2 / sum(ponderation)
        # print("{:.4f}".format(average2))

        moy_deriv3 = 0
        for x, y in zip(dy_dx3_clean, ponderation):
            moy_deriv3 += x * y

        average3 = moy_deriv3 / sum(ponderation)
        # print("{:.4f}".format(average3))


        # print("{:.4f}".format(moy_deriv1), "{:.4f}".format(moy_deriv2), "{:.4f}".format(moy_deriv3))

        impact_inverse = [moy_deriv1, moy_deriv2]
        augmente = 0
        diminue = 0
        neutre = 0

        #résultats
        #impact direct du temps
        if moy_deriv3 > 0:
            augmente += 1
        elif moy_deriv3 < 0:
            diminue += 1
        elif moy_deriv3 == 0:
            neutre += 1


        #impact inverse de la température et de la luminosité
        for i in impact_inverse:
            if i < 0 :
                augmente += 1
            elif i > 0 :
                diminue += 1
            elif i == 0 :
                neutre += 1

        probabilités_augmente = (augmente/3)*100
        probabilités_diminue = (diminue/3)*100
        probabilités_neutre = (neutre/3)*100

        # print("Il y a ", "{:.2f}".format(probabilités_augmente)," % que l'humidité ambiante augmente.")
        # print(f"Il y a ", "{:.2f}".format(probabilités_diminue)," % que l'humidité ambiante diminue.")
        # print(f"Il y a ", "{:.2f}".format(probabilités_neutre)," % que l'humidité ambiante ne varie pas.")

        var=[probabilités_augmente,probabilités_diminue,probabilités_neutre]
        return var #renvoi les données




    def temperature(self, data, plante_n):

        plante=(f"Capteur {plante_n}")
        # print (plante)

        # print(data)
        data['Date'] = pd.to_datetime(data['Date'])
        x = data['Date'].dt.strftime("%H:%M")
        xf = pd.to_datetime(x, format="%H:%M").dt.time
        x_base_10 = np.array([t.hour + t.minute / 60 for t in xf], dtype=float)
        for i in range(len(data)):
            if x_base_10[i-1] > x_base_10[i]:
                for k in range(i, 95):
                    x_base_10[k] = x_base_10[k]+24
        if x_base_10[k] == x_base_10[0]:
            for j in range(k, 95):
                x_base_10[j] = x_base_10[j]-24

        x1 = np.array(data['Humidité ambiante'], dtype=float)
        x2 = np.array(data['Clear'], dtype=float)
        y = np.array(data[plante], dtype=float)

        #ajout de précision des résultats en prenant seulement les dernières valeurs
        x_base_10 = x_base_10[88:]
        x1 = x1[88:]
        x2 = x2[88:]
        y = y[88:]

        ponderation = [1, 2, 3, 4, 7, 8, 9, 10, 11]

        #calculs dérivées
        try:
            dy_dx1 = np.gradient(y, x1)
            dy_dx2 = np.gradient(y, x2)
            dy_dx3 = np.gradient(y, x_base_10)
        except ZeroDivisionError:
            print("ERREUR : Division par zéro dans le calcul de la dérivée")

        dy_dx1_clean = np.where(np.isfinite(dy_dx1),dy_dx1,0)
        dy_dx2_clean = np.where(np.isfinite(dy_dx2),dy_dx2,0)
        dy_dx3_clean = np.where(np.isfinite(dy_dx3),dy_dx3,0)


        # print(dy_dx1_clean, dy_dx2_clean, dy_dx3_clean)

        moy_deriv1 = 0
        for x, y in zip(dy_dx1_clean, ponderation):
            moy_deriv1 += x * y

        average1 = moy_deriv1 / sum(ponderation)
        # print("{:.4f}".format(average1))

        moy_deriv2 = 0
        for x, y in zip(dy_dx2_clean, ponderation):
            moy_deriv2 += x * y

        average2 = moy_deriv2 / sum(ponderation)
        # print("{:.4f}".format(average2))

        moy_deriv3 = 0
        for x, y in zip(dy_dx3_clean, ponderation):
            moy_deriv3 += x * y

        average3 = moy_deriv3 / sum(ponderation)
        # print("{:.4f}".format(average3))


        # print("{:.4f}".format(moy_deriv1), "{:.4f}".format(moy_deriv2), "{:.4f}".format(moy_deriv3))

        impact_direct = [moy_deriv2, moy_deriv3]
        augmente = 0
        diminue = 0
        neutre = 0

        #résultats
        #luminosité et temps impact direct 
        for i in impact_direct:
            if i > 0 :
                augmente += 1
            elif i < 0 :
                diminue += 1
            elif i == 0 :
                neutre += 1

        #impact inverse de l'humidité ambiante
        if moy_deriv1 < 0:
            augmente += 1
        elif moy_deriv1 > 0 :
            diminue += 1
        elif moy_deriv1 == 0 :
            neutre += 1

        probabilités_augmente = (augmente/3)*100
        probabilités_diminue = (diminue/3)*100
        probabilités_neutre = (neutre/3)*100

        # print("Il y a ", "{:.2f}".format(probabilités_augmente)," % que la température augmente.")
        # print(f"Il y a ", "{:.2f}".format(probabilités_diminue)," % que la température diminue.")
        # print(f"Il y a ", "{:.2f}".format(probabilités_neutre)," % que la température ne varie pas.")

        var=[probabilités_augmente,probabilités_diminue,probabilités_neutre]
        return var #renvoi les données


    

# allo = Predictions(data, plante) 

