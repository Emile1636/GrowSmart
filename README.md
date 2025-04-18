# GrowSmart
<img width="1470" alt="Capture d’écran, le 2025-01-26 à 21 06 50" src="https://github.com/user-attachments/assets/805af699-397a-409a-9d8a-bfcbeed4ef3c" />

## Description

<p>
<strong>GrowSmart</strong> est une application qui améliore la gestion de vos plantes à domicile.  
Simple et intuitive, elle optimise la croissance de vos plantes et <strong>vous accompagne dans leur entretien</strong>.
<p align="justify">
<strong>GrowSmart</strong> fonctionne en récoltant des données sur vos plantes afin d'analyser leur environnement. Une multitude d'outils sera alors à votre disposition pour suivre leur développement et favoriser leur croissance. L'objectif est simple : vous accompagner dans leur entretien afin de leur offrir un soin optimal, <strong>le soin qu'elles méritent</strong>.
</p>

## Fonctionnalités & aspect évolutif

| Fonctionnalités de base| Évolutions prioritaires|Évolutions secondaires|
| :-------------:|:-------------:|:-----:|
| Gestion des profiles| Récolte des données en temps réel | Arrosage avec pompe à eau |
| Analyse des données| Implémenter des alertes| Conseiller selon les données récoltées |
| Visualisation des données | - | Alimentation par énergie solaire |

## Intégrations des notions scientifiques

### Mathématiques discrètes
 - **Chiffrement RSA** : Chiffrer les informations de connexion des utilisateurs
 - **Graph** : Représentation visuel en tout genre sur les plantes et leur environnement 
### Calcul différentiel 
 - **Dériver et taux de variation** : Détecter l'intensiter des variations de l'environnement afin d'alerter l'utilisateur
 - **Prédications grâce aux fonctions** : Prédire les fluctuations de l'environnement
### Ondes et physique moderne
 - **Énergie des photons** : Mesurer la quantité d'énergie brut émise par la lumière et la représenter graphiquement

> [!NOTE]
> L'implémentation des notions scientifiques est l'objectif au coeur du projet.

## Technologies embarqués

### Capteurs
 - Capteur d'humidité du sol : *Capacitive soil moisture sensor v1.2*
 - Capteur de température et d'humidité ambiant : *DHT22*
 - Capteur d'intensité lumineuse : *BH1750FVI*
 - Capteur de couleur spectrale : *AS7341*
### Contrôleurs
 - Arduino Mega
 - Raspberry Pi 5
### Accesoires
 - Cables divers, résistances et platine d'expérimentation (*breadboard*)

> [!NOTE]
> <p align="justify">Les données sont récoltées par les capteurs toutes les 15 minutes. Les informations brutes, une fois traitées par l'Arduino, sont alors envoyées au Raspberry Pi. Celui-ci actualise alors un fichier CSV accessible par tous et consultable en ligne contenant les données traitées une première fois. L'application se charge alors de récolter ces données, de les associer à l'utilisateur et de les analyser. À noter qu'un historique de 24 h est consultable au maximum, soit 96 prises de données.</p>

## Contexte et objectif

Ce projet fait partie d'un cours de fin de parcours où l'application des apprentissage spécifique au programme de SIM *(Sciences informatique et mathématiques)* est l'objectif principale. Merci de votre compréhension.
