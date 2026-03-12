import LoRa1
import numpy as np

#"fini" il faut modifier avec LoRa, peut etre que delay peut etre plus cours que 15min lire des etudes


#def pingmedecin(): #a ecrire
    #print('mort')
valeur=np.zeros((3,30))
delay = np.array([[valeur.copy(), 0] for _ in range(30)], dtype=object)  # 30 × (None, 0) # On stocke des objets (tableaux) dedans

def f_verification(delay):
    incoming = LoRa1.get_latest_entry()
    if incoming.any():  # Vérifie si la ligne n'est pas vide
        # Sépare les données en fonction de la virgule et les convertit en float
        donnee1, donnee2, donnee3 = incoming
        valeur=delay[0][0].copy()
        for i in range(29, 0, -1):  
            valeur[:,i] = valeur[:,i-1]
        # Insère les nouvelles données dans la première ligne
        valeur[:,0] = [donnee1, donnee2, donnee3]
        donnee1=valeur[0][0]
        for i in range(29, 0, -1):  
            delay[i] = delay[i-1]
        delay[0][0]=valeur.copy()
        if donnee1<10:
            for i in range(30):
                delay[i][1] = 1
        else:
            delay[0][1]=0
    return delay



#delay=f_verification(delay.copy())