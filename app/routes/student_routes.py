from flask import Blueprint, render_template, request, redirect, session
from app.models.student_model import find_student
from app.models.questionnaire_model import create_questionnaire, find_questionnaires_by_student

student_bp = Blueprint('student', __name__)

@student_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        student = find_student(username)
        if student and student['password'] == password:
            session['student'] = username
            return redirect('/student/my-questionnaires')
        else:
            return render_template('login.html', error="Λάθος στοιχεία")
    return render_template('login.html')

@student_bp.route('/logout')
def logout():
    session.pop('student', None)
    return redirect('/')

@student_bp.route('/create', methods=['GET', 'POST'])
def create_questionnaire_view():
    if 'student' not in session:
        return redirect('/student/login')

    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        questions = []
        for i in range(1, 6):  # Έως 5 ερωτήσεις ως παράδειγμα
            q_text = request.form.get(f'q{i}')
            if q_text:
                questions.append({
                    "type": "Open Ended",
                    "description": q_text,
                    "question_num": i
                })

        create_questionnaire(session['student'], title, description, questions)
        return redirect('/student/my-questionnaires')

    return render_template('create_questionnaire.html')

@student_bp.route('/my-questionnaires')
def my_questionnaires():
    if 'student' not in session:
        return redirect('/student/login')

    questionnaires = find_questionnaires_by_student(session['student'])
    return render_template('view_questionnaires.html', questionnaires=questionnaires)
