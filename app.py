from flask import Flask, render_template, request, redirect, url_for
import csv
import os
from datetime import datetime
from new import createQuestion
from review import filter_questions_by_retention, filter_questions_ids, edit_level

app = Flask(__name__)


#Route du menu principal
@app.route("/")
def menu():
    return render_template("index.html")


#Route pour créer une nouvelle connaissance
@app.route("/new",)
def new():
    return render_template('new.html')


#Route pour envoyer la connaissance au script python
@app.route("/dataprocessing", methods=["POST", "GET"])
def dataProcessing():

    if request.method == "POST":

        getData = request.form
        newData = getData.get('newData')

        #Envoie la nouvelle donnée à new.py pour créer une nouvelle question, et la stocker dans data.csv
        createQuestion(newData)

        return redirect(url_for('success', via_redirect=True))
    
    else:
        return redirect(url_for('menu'))


#Route pour afficher le succès de l'enregistrement de la connaissance
@app.route("/success")
def success():

    #Vérifie si la requête provient de dataprocessing, sinon redirect vers menu
    if request.args.get('via_redirect'):
        return render_template('success.html')
    else:
        return redirect(url_for('menu'))


#Route pour accéder au mode révision
@app.route("/reviewer", methods=["POST", "GET"])
def reviewer():

    current_question = None
    questions = []
    questions_id = []

    #Rajoute au fichier csv les nouvelles questions à traiter de la journée
    filter_questions_by_retention()

    #Appel review.py pour récuperer les IDs des questions à réviser
    questions_id = filter_questions_ids()

    #Renvoie les questions en fonction des IDs fournies
    with open('data.csv', mode='r', encoding='utf-8') as csvfile:
        csvreader = csv.DictReader(csvfile)
        # Parcourir chaque ligne du fichier CSV
        for row in csvreader:
            # Si l'ID de la ligne est dans la liste des IDs spécifiés
            if row['id'] in questions_id:
                # Créer un dictionnaire avec les champs désirés et l'ajouter à la liste de résultats
                filtered_row = {
                    'question': row['question'],
                    'answer': row['answer'],
                    'level': row['level']
                }
                questions.append(filtered_row)

    #Affecte la première question de la liste de questions
    if questions:
        current_question = questions[0]

    #Vérifie si la page est demandée via une requête POST ou pas, si question_id a un élement, et affiche la réponse ou question en fonction
    if request.method == "POST" and 'client_response' in request.form and questions_id:
        print("Client self-reviewed")
        #Vérifie si la réponse de l'utilisateur est vraie ou fausses
        response = request.form['client_response'] == 'true'
        #Met à jour le level de la connaissance + retire l'ID de la liste
        edit_level(response, questions_id[0])

        #filter_questions_by_retention()

        return redirect(url_for('reviewer'))


    return render_template('reviewer.html', question=current_question)



#Route pour accéder à la bibliothèque des connaissances
@app.route("/database")
def database():
    
    data = []

    if os.path.exists("data.csv"):

        with open('data.csv', newline='') as csvfile:
        # Créer un lecteur CSV
            reader = csv.reader(csvfile)
        
            # Ignorer la première ligne (les en-têtes)
            next(reader)
            
            # Lire chaque ligne du fichier CSV
            for row in reader:
                # Ajouter la ligne au tableau
                data.append([row[0], row[1], row[2], row[3]])

    return render_template("database.html", dataList=data)


if __name__ == "__main__":
    app.run(debug=True)