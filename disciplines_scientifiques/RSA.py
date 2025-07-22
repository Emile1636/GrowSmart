import sympy
import random
import json
import secrets
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
class RSA: # class pour chiffrer le mot de passe en RSA
    def __init__(self, master):
        self.master = master
        
    def Trouver_premier(): #Trouve un nombre premier
        premier=False
        while premier!=True:  # recommence à générer des nombre aléatoire tant que celui ci n'est pas premier
            n=secrets.randbits(256)# chioisi un nombre random de 256 bits #vrai aléatoire cryptographique
            premier=sympy.isprime(n) # Vérifie si le nombre random est premier
        return n

    def Créer_clé(): #chiffre le mots de passe reçu en RSA
        
        p=RSA.Trouver_premier() #trouve un p aléatoire
        q=RSA.Trouver_premier() #trouve un q aléatoire

        while p==q: #vérifie que p n'est pas égale à q
            q=RSA.Trouver_premier() #trouve un nouveau q
        
        n=p*q #calcule le n (clé publique)
        phi=(p-1)*(q-1) #calcule le phi utiliser
        e=65537 #calcule le e (clé publique )

        if phi%e==0: #vérifie que phi n'est pas un multiple de e
            return(RSA.Créer_clé()) #Retourne les nouvelles valeurs obtenus
        
        # d=sympy.mod_inverse(e,phi) #Calcule d (clé privé)

        return(e,n) #retourne la clé public  et privé
    
    def chiffrer(MDP,e,n):
        MDP_RSA=[pow(ord(let),e,n) for let in MDP] #chiffre le mot de passe non chiffrer
        return MDP_RSA
    
    # def déchiffrer(MDP_RSA,d,n):
    #     MDP="".join([chr(pow(nb,d,n)) for nb in MDP_RSA])  #Permet de déchiffrer un mot de passe
    #     return MDP

    def noter_nouv_élém(utili, MDP): #note le mot de passe chiffrer avec les clés pblics et privée
        e,n=RSA.Créer_clé()        #

        with open("users.json", "r") as f: # Récuéperer les identifiants des utilisateurs
            liste_utilisateurs = json.load(f)      #récupère les données nécessaires

        MDP_RSA=RSA.chiffrer(MDP,e,n)       #chiffre le mot de passe

        liste_utilisateurs[utili] = {"password": MDP_RSA, "Cle public e": e, "Cle public n": n} 
        with open("users.json", "w") as f:
            json.dump(liste_utilisateurs, f, indent=4)# importe les données dans user.json

    def vérifier_mot(utili,mot):   #Transforme le mot de passe entrer en code RSA

        with open("users.json", "r") as f: # Récuéperer les identifiants des utilisateurs
            liste_utilisateurs = json.load(f)      #récupère les données nécessaires
        
        e=liste_utilisateurs[utili]["Cle public e"]#Va chercher les clées publics de l'utilisateur
        n=liste_utilisateurs[utili]["Cle public n"]#

        # print(RSA.déchiffrer(liste_utilisateurs[utili]["password"],liste_utilisateurs[utili]["Cle prive d"],n)) #Test la fonction déchiffrer

        return RSA.chiffrer(mot,e,n)  #renvoi le mot en RSA
    
    







           
            



        
        
        
        




