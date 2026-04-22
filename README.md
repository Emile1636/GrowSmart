# 🌿 GrowSmart

<img width="1470" alt="Capture d’écran GrowSmart" src="https://github.com/user-attachments/assets/805af699-397a-409a-9d8a-bfcbeed4ef3c" />

---

## 📌 Description

**GrowSmart** est une application innovante qui simplifie la gestion et l’entretien des plantes d’intérieur.  
Elle s’appuie sur un réseau de capteurs pour analyser en temps réel l’environnement de vos plantes, visualiser les données de croissance et **vous accompagner au quotidien** pour leur offrir les meilleurs soins.

Des capteurs reliés à un **Arduino Mega** et un **Raspberry Pi** collectent :
- l’humidité du sol
- l’humidité et la température ambiantes
- l’intensité et la qualité de la lumière (spectre lumineux)

Toutes ces données sont traitées, stockées et affichées sous forme de **graphiques dynamiques** et de **tableaux interactifs** (DataFrame) pour suivre les tendances, détecter les variations et ajuster l’entretien.

---

## ⚙️ Fonctionnalités & Évolutivité

| Fonctionnalités de base | Évolutions prioritaires | Évolutions futures |
| :---------------------: | :---------------------: | :----------------: |
| Création de profils sécurisés (RSA) | Collecte de données en temps réel | Arrosage automatisé via pompe |
| Analyse des données (graphiques, dérivées) | Système d’alertes personnalisées | Conseils automatiques basés sur l’historique |
| Visualisation claire et intuitive | - | Alimentation par panneaux solaires |

<img alt="Formulaire" src="https://github.com/user-attachments/assets/87d0f74c-a190-47f2-9b52-675986a00beb" width="49%" style="float: left;">
<img alt="Inscription" src="https://github.com/user-attachments/assets/ccc81b69-21e0-4c96-a523-27db21ba47af" width="49%" style="float: left;">

---

## 🧩 Intégrations scientifiques

### Mathématiques discrètes
- **Chiffrement RSA** : Sécurisation des informations de connexion.
- **Théorie des graphes** : Représentation visuelle des liens entre paramètres environnementaux.

### Calcul différentiel
- **Dérivées et taux de variation** : Détection des variations anormales.
- **Prédictions** : Estimation des fluctuations futures de l’environnement.

### Ondes et physique moderne
- **Énergie des photons** : Calcul de l’énergie lumineuse absorbée par la plante grâce à l’analyse spectrale.

<img width="60%" alt="Energie" src="https://github.com/user-attachments/assets/4914f75f-a40d-41c4-9c8f-cf68e8295d20" />

> [!NOTE]
> *Les notions scientifiques appliquées sont au cœur de la valeur ajoutée du projet.*

---

## 🔌 Technologies & Matériel

### Capteurs
- *Capacitive soil moisture sensor v1.2* : humidité du sol
- *DHT22* : température et humidité ambiantes
- *BH1750FVI* : intensité lumineuse
- *AS7341* : spectre de la lumière

### Contrôleurs
- Arduino Mega
- Raspberry Pi 5

### Accessoires
- Breadboard, câbles, résistances diverses.

### Figure du circuit
<img width="75%" alt="Montage copie" src="https://github.com/user-attachments/assets/e08f60c4-994d-4dc4-a4f9-56ad14b4e3dc" />

> [!NOTE]
> *Les données sont relevées toutes les **15 minutes**, stockées dans un fichier CSV mis à jour par le Raspberry Pi, puis traitées et affichées dans l’application.* \
> <img width="50%" alt="raspberry interface" src="https://github.com/user-attachments/assets/d74dd76a-5906-4d73-b6b0-27df642771af">


---

## 🎓 Contexte pédagogique

**GrowSmart** est un projet développé dans le cadre d’un cours de fin d’études du programme **Sciences informatiques et mathématiques (SIM)**.  
L’objectif est de **mobiliser concrètement** des connaissances théoriques (maths, physique, algorithmique) dans une application **utile et fonctionnelle**.

---

<!-- ## 📎 Liens utiles -->

<!-- - [Vidéo démonstrative](https://drive.google.com/file/d/1M_vgP-oa0pE34ki26zvUVhoOBK-4dBAW/view?usp=sharing) -->

<!-- --- -->

 *Merci de votre intérêt pour GrowSmart !*
