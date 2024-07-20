import pandas as pd
import os
import csv
from datetime import datetime, timedelta

delayedData = []

# Vérifie si le fichier "DelayeddDta.csv" existe
if not os.path.exists("delayedData.csv"):
    # Crée un nouveau fichier "DelayedData.csv"
    with open("delayedData.csv", mode="w", newline="", encoding='utf-8') as file:
        writer = csv.writer(file)
        #writer.writerow(["id"])
    print("delayedData.csv file created.")


if os.path.exists("data.csv"):
    # Lire le fichier CSV
    data = pd.read_csv('data.csv', sep=',', encoding="utf-8")
    # Convertir la colonne 'date' en datetime
    data['date'] = pd.to_datetime(data['date'])



#Dictionnaire du nombre de jour de rétention de l'information en fonction du level
retention = {
    0: 0.7,
    1: 3,
    2: 7,
    3: 14,
    4: 31,
    5: 186
}


def filter_questions_by_retention():

    data = []

    # Date actuelle
    now = datetime.now()

    if os.path.exists("data.csv"):
        # Lire le fichier CSV
        data = pd.read_csv('data.csv', sep=',', encoding="utf-8")
        # Convertir la colonne 'date' en datetime
        data['date'] = pd.to_datetime(data['date'])

    
    if os.path.exists("delayedData.csv"):

        existing_ids = []

        # Lire les IDs existants dans le fichier CSV
        with open("delayedData.csv", mode="r", newline="", encoding='utf-8') as file:
            reader = csv.reader(file)
            for row in reader:
                if len(row) > 0:  # Vérifier que la ligne contient au moins un élément
                    existing_ids.append(row[0])

        # Parcourir les lignes du DataFrame
        for index, row in data.iterrows():
            print(row['level'])
            # Calculer la différence en jours entre la date actuelle et la date de l'entrée
            days_diff = ((now - row['date']).total_seconds())/86400
            
            print(days_diff, retention[row['level']])

            # Vérifier si la différence en jours est égale au nombre de jours de rétention pour ce niveau
            if days_diff >= retention[row['level']]:

                # Ajouter le nouvel ID seulement s'il n'est pas déjà présent
                if row['id'] not in existing_ids:
                    with open("delayedData.csv", mode="a", newline="", encoding='utf-8') as file:
                        writer = csv.writer(file)
                        writer.writerow([row['id']])
                        print(f"ID : {row['id']} has been added to delayedData.csv")
                else:
                    print(f"ID : {row['id']} already exists in delayedData.csv")


#Fonction qui récupère les ID des questions à réviser
def filter_questions_ids():

    list_questions_ids = []

    with open('delayedData.csv', newline='') as csvfile:
        reader = csv.reader(csvfile)
        
        # Lire chaque ligne et ajouter l'id à la liste
        for row in reader:
            if len(row) > 0:
                list_questions_ids.append(row[0])
        
    return list_questions_ids


#Fonction pour supprimer l'ID d'une question dans delayedData.csv
def remove_question_id(id_to_remove):

    temp_filename = 'temp.csv'
    
    with open("delayedData.csv", newline='') as csvfile, open(temp_filename, 'w', newline='') as temp_csvfile:
        reader = csv.reader(csvfile)
        writer = csv.writer(temp_csvfile)
        
        #Vérifie si chaque row n'est pas l'ID à remove
        for row in reader:
            if row and row[0] != id_to_remove:
                writer.writerow(row)
    
    # Remplacer le fichier original par le fichier temporaire
    os.replace(temp_filename, "delayedData.csv")
    print(f"ID '{id_to_remove}' has been removed if it existed.")


#Fonction pour mettre à jour le level d'une connaissance
def edit_level(isLearned, id):

    # Lire le fichier CSV
    df = pd.read_csv('data.csv')
    # Trouver l'index de la ligne avec l'id spécifié
    index = df[df['id'] == id].index

    if not index.empty:

        if isLearned:
            # Incrémenter le niveau de 1 si isLearned est True
            df.at[index[0], 'level'] += 1
            print("Level increased")

        else:
            # Réinitialiser le niveau à 0 si isLearned est False
            df.at[index[0], 'level'] = 0

            print("Level and reset")

        #Retire l'ID de la liste
        remove_question_id(id)

        # Mettre à jour la date
        df.at[index[0], 'date'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print("Date reset")

        # Sauvegarder les modifications dans le fichier CSV
        df.to_csv('data.csv', index=False)
    
    else:
        print(f"ID {id} non trouvé dans le fichier.")
