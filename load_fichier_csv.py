import pandas as pd
import requests
from pathlib import Path
from io import StringIO

# Obtenir l'URL fixe du Gist (stockée dans 'gist_url.txt')
def get_gist_url():
    url_path = Path(__file__).parent / 'gist_url.txt'
    with open(url_path, 'r') as f:
        return f.read().strip()

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
    gist_url = get_gist_url()

    if not gist_url:
        print("URL du Gist introuvable.")
        return None
    
    csv_content = download_csv_from_gist(gist_url)
    print(csv_content)
    
    if csv_content:
        column_names = ['Capteur 1', 'Capteur 2', 'Capteur 3', 'Capteur 4', 'Capteur 5', 'Humidité ambiante', 'Température', 'Luminosité']
        data = pd.read_csv(StringIO(csv_content), header=None, names=column_names)
        return data
    else:
        print("Échec du téléchargement du fichier CSV.")
        return None

# Exemple d'utilisation
data = load_data_from_gist()
    
if data is not None:
    print("Données chargées avec succès :")
    print(data.head())
