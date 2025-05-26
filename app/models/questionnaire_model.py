from app import mongo
import random

def get_all_questionnaires():
    return list(mongo.db.questionnaires.find())

def find_questionnaire_by_id(questionnaire_id):
    return mongo.db.questionnaires.find_one({"questionnaire_id": questionnaire_id})

def find_questionnaires_by_student(username):
    return list(mongo.db.questionnaires.find({"creator_username": username}))

def get_all_questionnaires_sorted(order='desc'):
    sort_order = -1 if order == 'desc' else 1
    return list(mongo.db.questionnaires.find().sort("answer_count", sort_order))

def search_questionnaires(filters):
    query = {}

    # Φίλτρο τίτλου
    if 'title' in filters and filters['title']:
        query['title'] = {'$regex': filters['title'], '$options': 'i'}  # case-insensitive

    # Φίλτρο φάσματος απαντήσεων
    answer_range = {}
    if filters.get('min_answers'):
        answer_range['$gte'] = int(filters['min_answers'])
    if filters.get('max_answers'):
        answer_range['$lte'] = int(filters['max_answers'])
    if answer_range:
        query['answer_count'] = answer_range

    # Φίλτρο φοιτητή (όνομα ή reg_number)
    if filters.get('student_name'):
        # Βρίσκουμε τους φοιτητές με αυτό το όνομα
        students = list(mongo.db.students.find({'name': {'$regex': filters['student_name'], '$options': 'i'}}, {'_id': 0, 'reg_number': 1}))
        reg_numbers = [s['reg_number'] for s in students]
        query['student_id'] = {'$in': reg_numbers}

    # Φίλτρο τμήματος
    if filters.get('department'):
        students = list(mongo.db.students.find({'department': {'$regex': filters['department'], '$options': 'i'}}, {'_id': 0, 'reg_number': 1}))
        reg_numbers = [s['reg_number'] for s in students]
        query['student_id'] = {'$in': reg_numbers} if 'student_id' not in query else {'$in': list(set(query['student_id']['$in']) & set(reg_numbers))}

    return list(mongo.db.questionnaires.find(query))