import numpy as np
import verification2
import time 

data=[]
valeur=np.zeros((3,30))
delay = np.array([[valeur.copy(), 0] for _ in range(30)], dtype=object)  # 30 × (None, 0) # On stocke des objets (tableaux) dedans

def f_donnees1(delay,data):
    delay=verification2.f_verification(delay)
    data.append(delay[-1].copy())
    time.sleep(30)  #il faut mettre 30
    return delay,data

#delay,data=f_donnees1(delay.copy(),data.copy())

