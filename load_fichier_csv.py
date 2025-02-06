import pandas as pd
import requests
from pathlib import Path
from io import StringIO

def get_raw_url_from_gist_api(gist_id):
    # Récupère l'URL brute du fichier CSV à partir du Gist via l'API GitHub
    url = f"https://api.github.com/gists/{gist_id}"
    response = requests.get(url)
    
    if response.status_code == 200:
        # Extraire l'URL brute du fichier CSV depuis la réponse de l'API
        gist_data = response.json()
        
        # Assurez-vous que le fichier 'data.csv' existe dans le Gist
        if 'data.csv' in gist_data['files']:
            raw_url = gist_data['files']['data.csv']['raw_url']
            return raw_url
        else:
            print("Le fichier 'data.csv' n'est pas trouvé dans ce Gist.")
            return None
    else:
        print(f"Erreur lors de l'accès à l'API du Gist : {response.status_code}")
        return None

# Télécharger le fichier CSV depuis l'URL du Gist
def download_csv_from_gist(gist_url):
    response = requests.get(gist_url)
    if response.status_code == 200:
        content = response.text
        return content
    else:
        print(f"Erreur lors du téléchargement : {response.status_code}")
        return None

# Charger les données CSV dans un Dataframe pandas
def load_data_from_gist():
    gist_url = get_raw_url_from_gist_api(gist_id)

    if not gist_url:
        print("URL du Gist introuvable.")
        return None
    
    csv_content = download_csv_from_gist(gist_url)

    if csv_content:
        column_names = ['Capteur 1', 'Capteur 2', 'Capteur 3', 'Capteur 4', 'Capteur 5', 'Humidité ambiante', 'Température', 'Luminosité']
        data = pd.read_csv(StringIO(csv_content), header=None, names=column_names)
        return data
    else:
        print("Échec du téléchargement du fichier CSV.")
        return None
''' 

Les données sont récoltées par les capteurs tous les 15 minutes. 
À noter qu'un historique de 24h est consultable au maximum, soit 96 prises de données.

'''
# Exemple d'utilisation
gist_id = "9d24cf5e4b6accfcf7d73615c595889d"  # ID du Gist
data = load_data_from_gist()

if data is not None:
    print("Données chargées avec succès :")
    print(data.head()) # 5 premières lignes (il y à 24h et moins)
    print(data.tail()) # 5 dernières lignes (il y à 15min et plus)
