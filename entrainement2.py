from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay
from sklearn.metrics import precision_score, recall_score, f1_score
import matplotlib.pyplot as plt
import torch
import torch.nn as nn
import données1
import numpy as np
import time
#import data_initiale #fichier a creer independant du patient

valeur=np.zeros((3,30))
delay = np.array([[valeur.copy(), 0] for _ in range(30)], dtype=object)  # 30 × (None, 0) # On stocke des objets (tableaux) dedans


#modèle de reseau de neurones CNN1D pour reveler des dependances temporelles, a voir si on trouve mieux
model = nn.Sequential(
nn.Conv1d(in_channels=3, out_channels=16, kernel_size=3, stride=1),  # Traite 3 capteurs comme des "canaux"
nn.ReLU(),
nn.MaxPool1d(kernel_size=2),
nn.Flatten(),
nn.Linear(224, 64),  # Ajustez cette taille en fonction de la sortie du CNN
nn.ReLU(),
nn.Linear(64, 2)
)


# Fonction de perte et optimiseur, à optimiser
# Classe 0 = patient sain (moins important à prédire correctement)
# Classe 1 = patient en crise (très important à prédire correctement)
weights = torch.tensor([1.0, 5.0], dtype=torch.float32)  # à ajuster intelligement, 5 étant pris au pif, rend plus important les faux negatifs (car graves) que les faux positifs(moins graves)
loss_function = nn.CrossEntropyLoss(weight=weights)


optimizer = torch.optim.Adam(model.parameters())


# Entraînement du modèle
epochs = 1000 #à optimiser
losses = []
accuracies = []
generation=0

def evaluate_model(model):
    outputs = model(X_test_torch)
    _, predicted_labels = torch.max(outputs, 1)  # Trouver l'étiquette prédite
    accuracy = (predicted_labels == y_test_torch).sum().item() / len(y_test_torch)
    return accuracy

def save_model(model, generation):
    filename = f"model_generation_{generation}.pt"
    torch.save(model.state_dict(), filename)
    print(f"Modèle sauvegardé dans : {filename}")


start_time = time.perf_counter()

while True:

    data=[]
    
    while time.perf_counter()-start_time< 86400 : #1journée
        delay,data=données1.f_donnees1(delay,data)

    start_time = time.perf_counter()
    generation+=1

    # Extraction des données

    donnee1 =[data[i][0][0] for i in range(len(data))]
    donnee2 =[data[i][0][1] for i in range(len(data))]
    donnee3 =[data[i][0][2] for i in range(len(data))]
    target=[data[i][1] for i in range(len(data))]
    
    X = np.array([
        np.stack((donnee1[i], donnee2[i], donnee3[i])
        for i in range(len(donnee1)))
    ])  # -> shape (N, 3, 30)
    
    # X a la forme (N, 3, 30) — N patients, 3 capteurs, 30 mesures temporelles
    means = X.mean(axis=(0, 2))  # moyenne sur tous les patients et le temps → shape: (3,)
    stds = X.std(axis=(0, 2))    # écart-type → shape: (3,)

    # X shape: (N, 3, 30)
    # Normalisation par capteur
    for c in range(3):  # pour chaque capteur
        X[:, c, :] = (X[:, c, :] - means[c]) / stds[c]


    y = np.array(target)

    # Séparation en données d'entraînement et de test
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    X_train_torch = torch.tensor(X_train, dtype=torch.float32)  # shape: (batch, 3, 30)
    X_test_torch = torch.tensor(X_test, dtype=torch.float32)
    y_train_torch = torch.tensor(y_train, dtype=torch.long)  # Utilisation de torch.long pour la classification
    y_test_torch = torch.tensor(y_test, dtype=torch.long)  # Utilisation de torch.long pour la classification


    # Boucle d'entraînement
    for epoch in range(epochs):
        outputs = model(X_train_torch)  # Calculer les prédictions du modèle
        loss = loss_function(outputs, y_train_torch)  # Calculer la loss
        losses.append(loss.item())
        
        optimizer.zero_grad()  # Mettre les gradients à 0
        loss.backward()  # Faire de la backpropagation
        optimizer.step()  # Appliquer la mise à jour des poids


        accuracy = evaluate_model(model)

        accuracies.append(accuracy)
   
    # Évaluation finale
    outputs = model(X_test_torch)
    _, predicted_labels = torch.max(outputs, 1)
    accuracy = (predicted_labels == y_test_torch).sum().item() / len(y_test_torch)
    n=0
    n1=0
    n2=0
    for i in range(len(predicted_labels)):
        if y_test_torch[i]==1:
            n2+=1
            if predicted_labels[i]==1:
                n1+=1
            else:
                n+=1

    print("generation",generation)
    print("crises non predites=",n)
    print("crises predites=",n1)
    print("crises totales=",n2)
    print("nombre de patients testés=",len(y_test_torch))

    # Afficher la précision finale
    print(f"Précision du modèle sur les données de test (précision guez car non pondérée) : {accuracy:.4f}")


    
    y_true = y_test_torch.cpu().numpy()
    y_pred = predicted_labels.cpu().numpy()
    
    precision = precision_score(y_true, y_pred)
    recall = recall_score(y_true, y_pred)
    f1 = f1_score(y_true, y_pred)

    #indicateurs de precisions mieux pour notre cas 
    print(f"Recall (sensibilité)      : {recall:.4f}  ← À maximiser")#c'est TP/(TP+FN), le nombre de crises detectee sur le nb de crises total
    print(f"Precision (précision)     : {precision:.4f}")#TP/(TP+FP) sert a limiter les faux positifs
    print(f"F1-score                   : {f1:.4f}")# moyenne harmonique des 2 precedents
    
    save_model(model, generation)


   
    
