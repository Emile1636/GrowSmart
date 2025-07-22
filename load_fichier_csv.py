import pandas as pd
import requests
from io import StringIO

# Cache global pour stocker les données CSV téléchargées
cached_data = None

def get_raw_url_from_gist_api(gist_id):
    # Récupère l'URL brute du fichier CSV à partir du Gist via l'API GitHub
    url = f"https://api.github.com/gists/{gist_id}"
    response = requests.get(url)
    
    if response.status_code == 200:
        gist_data = response.json()
        if 'data.csv' in gist_data['files']:
            raw_url = gist_data['files']['data.csv']['raw_url']
            return raw_url
        else:
            print("Le fichier 'data.csv' n'est pas trouvé dans ce Gist.")
            return None
    else:
        print(f"Erreur lors de l'accès à l'API du Gist : {response.status_code}")
        return None

def download_csv_from_gist(gist_url):
    # Télécharge le fichier CSV depuis l'URL brute du Gist
    response = requests.get(gist_url)
    if response.status_code == 200:
        content = response.text
        return content
    else:
        print(f"Erreur lors du téléchargement : {response.status_code}")
        return None

def load_data_from_gist():
    global cached_data
    # Si les données sont déjà en cache, on les retourne directement
    if cached_data is not None:
        return cached_data
    
    gist_url = get_raw_url_from_gist_api(gist_id)
    if not gist_url:
        print("URL du Gist introuvable.")
        return None

    csv_content = download_csv_from_gist(gist_url)
    if csv_content:
        column_names = [
            'Date', 
            'Capteur 1', 'Capteur 2', 'Capteur 3', 'Capteur 4', 'Capteur 5', 
            'Humidité ambiante', 'Température',
            'Violet_415nm', 'Indigo_445nm', 'Bleu_480nm', 'Cyan_515nm',
            'Vert_555nm', 'Jaune_590nm', 'Orange_630nm', 'Rouge_680nm',
            'Clear', 'NIR'
        ]
        data = pd.read_csv(StringIO(csv_content), header=None, names=column_names)
        cached_data = data
        return data
    else:
        print("Échec du téléchargement du fichier CSV.")
        return None

def load_data_limited(list_colonnes):
    data = load_data_from_gist()
    
    colonnes_existantes = [
        'Date', 
        'Capteur 1', 'Capteur 2', 'Capteur 3', 'Capteur 4', 'Capteur 5', 
        'Humidité ambiante', 'Température',
        'Violet_415nm', 'Indigo_445nm', 'Bleu_480nm', 'Cyan_515nm',
        'Vert_555nm', 'Jaune_590nm', 'Orange_630nm', 'Rouge_680nm',
        'Clear', 'NIR'
    ]
    
    colonnes_utiles = [col for col in list_colonnes if col in colonnes_existantes]
    if not colonnes_utiles:
        raise ValueError("Aucune colonne valide.")
    return data[colonnes_utiles]

gist_id = "9d24cf5e4b6accfcf7d73615c595889d"  # ID du Gist

'''
# Exemple d'utilisation 

data1 = load_data_from_gist()
data2 = load_data_limited(['Température', 'Violet_415nm', 'Vert_555nm', 'Rouge_680nm'])

if data1 is not None:
    print("Données complètes chargées avec succès :")
    print(data1.head()) # 5 premières lignes (il y à 24h et moins)
    print(data1.tail()) # 5 dernières lignes (il y à 15min et plus)

if data2 is not None:
    print("Données sélectives chargées avec succès :")
    print(data2.head()) # 5 premières lignes (il y à 24h et moins)
    print(data2.tail()) # 5 dernières lignes (il y à 15min et plus)
    
# Exemple d'analyse du spectre
if data1 is not None:
    # Calculer les moyennes du spectre sur la période
    moyennes_spectre = data1[['Violet_415nm', 'Indigo_445nm', 'Bleu_480nm', 'Cyan_515nm',
                              'Vert_555nm', 'Jaune_590nm', 'Orange_630nm', 'Rouge_680nm']].mean()
    print("Moyennes du spectre lumineux:")
    print(moyennes_spectre)
'''
