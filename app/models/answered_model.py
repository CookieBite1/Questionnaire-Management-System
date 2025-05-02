from app import mongo

# Αποθήκευση απαντήσεων σε ερωτηματολόγιο
def save_answered_questionnaire(questionnaire_id, from_student, answers):
    answered = {
        "questionnaire_id": int(questionnaire_id),
        "answered_by_student": from_student,
        "answers": answers
    }
    mongo.db.answered_questionnaires.insert_one(answered)

# Βρες όλες τις απαντήσεις για ένα ερωτηματολόγιο
def get_answers_for_questionnaire(qid):
    return list(mongo.db.answered_questionnaires.find({"questionnaire_id": int(qid)}))
