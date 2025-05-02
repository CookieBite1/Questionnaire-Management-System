from app import mongo
import random

def get_all_questionnaires():
    return list(mongo.db.questionnaires.find())

def find_questionnaire_by_id(questionnaire_id):
    return mongo.db.questionnaires.find_one({"questionnaire_id": questionnaire_id})

def find_questionnaires_by_student(username):
    return list(mongo.db.questionnaires.find({"creator_username": username}))

def create_questionnaire(username, title, description, questions):
    questionnaire_id = random.randint(10000, 99999)  
    questionnaire = {
        "questionnaire_id": questionnaire_id,
        "creator_username": username,
        "title": title,
        "description": description,
        "questions": questions,
        "answer_count": 0
    }
    mongo.db.questionnaires.insert_one(questionnaire)
