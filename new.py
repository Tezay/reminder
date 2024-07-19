import csv
import os
import hashlib
from datetime import datetime
from mistralai.client import MistralClient
from mistralai.models.chat_completion import ChatMessage
from config import API_KEY

promptSystem = "Tu es un assistant qui a pour unique but de synthétiser des informations sous forme de question-réponse, de sorte à pouvoir tester la connaissance. Pour chaque information donnée par l'utilisateur, répondre simplement \"Question : ...\" et \"Réponse : ...\". La réponse doit être la plus simple possible, il n'est pas nécessaire de reforumler la question."

model = "mistral-large-latest"

client = MistralClient(api_key=API_KEY)


#Génère une ID aléatoire en fonction de time
def generate_unique_id():
    current_time = str(datetime.now()).encode('utf-8')
    unique_id = hashlib.md5(current_time).hexdigest()
    return unique_id


def csvWriter(question, answer):
    # Vérifie si le fichier "data.csv" existe
    if not os.path.exists("data.csv"):
        # Crée un nouveau fichier "data.csv" avec les en-têtes
        with open("data.csv", mode="w", newline="", encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(["question", "answer", "date", "level", "id"])
        print("data.csv file created.")

    # Ajoute une nouvelle ligne au fichier
    with open("data.csv", mode="a", newline="", encoding='utf-8') as file:
        writer = csv.writer(file)
        current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        id = generate_unique_id()
        writer.writerow([question, answer, current_date, 0, id])
    print("Question/answer have been added to the data.csv file.")


def splitQuestionAswer(content):
    # Trouver les positions des mots-clés
    question_start = content.find("Question :")
    answer_start = content.find("Réponse :")
    
    # Extraire la question et la réponse
    question = content[question_start + len("Question :"):answer_start].strip()
    answer = content[answer_start + len("Réponse :"):].strip()
    
    return question, answer


def createQuestion(content):
    #Mistral AI API call
    response = client.chat(
    model=model,
    messages=[ChatMessage(role="user", content=promptSystem+content)]
    )
    print("Mistral AI API call completed.")

    question, answer = splitQuestionAswer(response.choices[0].message.content)
    csvWriter(question, answer)


#createQuestion("Il faut au maximum 25% d'une population pour lancer une révolution.")