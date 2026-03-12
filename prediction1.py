#!/usr/bin/python3
import numpy as np
import time
import torch
import firebase_admin
from firebase_admin import credentials, db
import LoRa1

# Initialise Firebase avec la clé du compte de service
cred = credentials.Certificate("C:/Users/felix/OneDrive/Bureau/projetsandbox2/serviceAccountKey.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://healthcare-true-default-rtdb.europe-west1.firebasedatabase.app/'
})





valeur=np.zeros((3,30))
delay = np.array([[valeur.copy(), 0] for _ in range(30)], dtype=object)  # 30 × (None, 0) # On stocke des objets (tableaux) dedans

start_time = time.perf_counter()


def prevision(valeur):
    incoming=LoRa1.get_latest_entry()
    if incoming.any():  # Vérifie si la ligne n'est pas vide
        # Sépare les données en fonction de la virgule et les convertit en float
        donnee1 = incoming[0]
        donnee2 = incoming[1]
        donnee3 = incoming[2]
        for i in range(29, 0, -1):  
            valeur[:,i] = valeur[:,i-1]
        # Insère les nouvelles données dans la première ligne
        valeur[:,0] = [donnee1, donnee2, donnee3]
    return valeur
        


def pingapp(data,pred):
    ref = db.reference('patients/patient_001')
    ref.set([data.tolist(),pred])


for _ in range(30):
    valeur=prevision(valeur)

def f_donnees1(data,last_value):
    data.append(last_value.copy())
    return data

data=[]

while True:
    generation=(time.perf_counter()-start_time)//86400
    valeur=prevision(valeur)
    model=model.load_state_dict(torch.load("model_generation_{generation}.pt"))
    pred=model(valeur)
    data=f_donnees1(data,valeur[0])
    pingapp(data,pred)
    time.sleep(30)







    


