# Prediction des arrêts cardiaques

Ce projet permet de collecter des données médicales via LoRa, de faire des prédictions à l’aide d’un réseau de neurones, et d’envoyer les résultats vers une base de données Firebase en temps réel.

## Il faut exécuter entrainement2.py et prediction1.py

`entrainement2.py` est le script construisant le modèle de prédiction

`prediction1.py` est le script principal qui :
- Récupère des données depuis un module LoRa (`LoRa1`),
- Met à jour une fenêtre glissante de 30 mesures (3 capteurs),
- Charge un modèle de prédiction ('entrainement2'),
- Effectue des prédictions,
- Envoie les données et les prédictions vers Firebase.



### Bibliothèques

Assurez-vous d’installer les modules suivants :

pip install torch firebase-admin numpy sklearn matplotlib time requests
