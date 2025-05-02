from flask import Blueprint, render_template, request, redirect
from app.models.questionnaire_model import get_all_questionnaires

user_bp = Blueprint('user', __name__)

@user_bp.route('/')
def index():
    return render_template('index.html')

@user_bp.route('/questionnaires')
def view_questionnaires():
    questionnaires = get_all_questionnaires()
    return render_template('view_questionnaires.html', questionnaires=questionnaires)

@user_bp.route('/questionnaire/<questionnaire_id>', methods=['GET'])
def view_questionnaire(questionnaire_id):
    from app.models.questionnaire_model import find_questionnaire_by_id
    questionnaire = find_questionnaire_by_id(int(questionnaire_id))
    return render_template('answer_questionnaire.html', questionnaire=questionnaire)

@user_bp.route('/questionnaire/<questionnaire_id>/submit', methods=['POST'])
def submit_answer(questionnaire_id):
    from app.models.answered_model import save_answered_questionnaire

    answers = []
    for key in request.form:
        answers.append({
            "question_num": int(key),
            "content": request.form[key]
        })

    save_answered_questionnaire(questionnaire_id, from_student=False, answers=answers)
    return redirect('/user/questionnaires')
