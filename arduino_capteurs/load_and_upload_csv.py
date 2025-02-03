import csv
import serial
import pandas as pd
import os
import requests
import json
from datetime import datetime
from pathlib import Path

# Obtenir le chemin absolu du repertoire contenant le code
SCRIPT_DIR = Path(__file__).parent.absolute()

def get_absolute_path(relative_path):
    # Reccuperer le chemin du fichier
    return os.path.join(SCRIPT_DIR, relative_path)

def gerer_limite_lignes(nom_fichier):
    # Verifie si le fichier contient plus de 10 lignes
    # Si oui, supprime la premiere ligne et decale les autres
    if not os.path.exists(nom_fichier):
        return
        
    df = pd.read_csv(nom_fichier, header=None)
    
    if len(df) > 96:
        df = df.iloc[1:].reset_index(drop=True)
        df.to_csv(nom_fichier, index=False, header=False)

def get_github_token():
    # Lire le token GitHub
    token_path = get_absolute_path('token_gits_growsmart.txt')
    with open(token_path, 'r') as f:
        return f.read().strip()

def get_gist_id():
    # Lire l'ID du Gist depuis le fichier gist_id.txt
    gist_id_path = get_absolute_path('gist_id.txt')
    if os.path.exists(gist_id_path):
        with open(gist_id_path, 'r') as f:
            return f.read().strip()
    return None

def save_gist_id(gist_id):
    # Sauvegarde l'ID du Gist 
    gist_id_path = get_absolute_path('gist_id.txt')
    with open(gist_id_path, 'w') as f:
        f.write(gist_id)

def upload_to_gist(csv_filename, gist_description="CSV Data Update"):
    # Upload ou met a jour le fichier CSV sur un Gist GitHub
    GITHUB_TOKEN = get_github_token()
    gist_id = get_gist_id()
    
    # Lire le contenu du fichier CSV
    with open(csv_filename, 'r') as file:
        content = file.read()
    
    gist_filename = "data.csv"
    headers = {
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "Accept": "application/vnd.github+json"
    }
    
    gist_data = {
        "description": f"{gist_description} - {datetime.now()}",
        "files": {
            gist_filename: {
                "content": content
            }}}
    
    if gist_id:
        # Si le Gist existe, on le met a jour 
        url = f"https://api.github.com/gists/{gist_id}"
        response = requests.patch(url, json=gist_data, headers=headers)
    else:
        # Si aucun Gist n'existe, on en cree un nouveau
        gist_data["public"] = True  # ou False pour un Gist prive
        url = "https://api.github.com/gists"
        response = requests.post(url, json=gist_data, headers=headers)
    
    if response.status_code in [200, 201]:
        gist_info = response.json()
        gist_id = gist_info['id']
        raw_url = gist_info['files'][gist_filename]['raw_url']
    
        # URL fixe du Gist 
        fixed_url = f"https://gist.github.com/{gist_id}"

        # Sauvegarde l'ID du Gist si il est cree
        if not get_gist_id():
            save_gist_id(gist_id)
    
        print(f"CSV upload avec succes. URL Gist (fixe) : {fixed_url}")
    
        # Sauvegarde l'URL fixe du Gist au lieu de raw_url
        url_path = get_absolute_path('gist_url.txt')
        with open(url_path, 'w') as f:
            f.write(fixed_url)
    
        return fixed_url
    else:
        print(f"Erreur lors de l'upload/mise a jour: {response.status_code}")
        print(f"Message: {response.text}")
        return None

def ajouter_donnees(nom_fichier, ligne_donnees):
    # Ajoute des donnees au CSV et gere la limite de lignes
    # Upload automatiquement vers Gist
    donnees = ligne_donnees.strip().split(',')
    
    if len(donnees) == 1:
        return
        
    if len(donnees) != 8:
        print("Erreur : il doit y avoir exactement 8 valeurs dans la ligne de donnees.")
        print(f"Donnees recues : {donnees}")
        return
    
    with open(nom_fichier, mode='a', newline='') as fichier:
        writer = csv.writer(fichier)
        writer.writerow(donnees)
    
    gerer_limite_lignes(nom_fichier)
    upload_to_gist(nom_fichier)
    print("Donnees ajoutees et uploadees:", donnees)

def collecte_continue(nom_fichier):
    # Collecte des donnees
    csv_path = get_absolute_path(nom_fichier)
    
    if not os.path.exists(csv_path):
        with open(csv_path, 'w', newline='') as f:
            pass
            
    while True:
        try:
            ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
            ligne_donnees = ser.readline().decode('utf-8', errors='replace').strip()
            ajouter_donnees(csv_path, ligne_donnees)
        except serial.SerialException as e:
            print(f"Erreur de connexion serie : {e}")
            break
        except Exception as e:
            print(f"Erreur inattendue : {e}")
            continue

if __name__ == "__main__":
    collecte_continue("donnees_capteurs.csv")
