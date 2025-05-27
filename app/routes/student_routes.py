from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from app.models.student_model import find_student
from app.models.questionnaire_model import find_questionnaires_by_student
from app.db.db_operations import get_db
from uuid import uuid4

student_bp = Blueprint('student', __name__)

@student_bp.route("/dashboard", endpoint="dashboard")
def dashboard():
    return render_template("student_dashboard.html")

@student_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        student = find_student(username)
        if student and student.get('password') == password:
            session['student'] = username
            session["reg_number"] = str(student["_id"])

            flash("Επιτυχής σύνδεση!", "success")
            return redirect(url_for('student.dashboard'))  # δική σου σελίδα
        else:
            flash("Λάθος στοιχεία!", "error")

    return render_template('login.html')

@student_bp.route('/logout')
def logout():
    session.clear()
    flash("Αποσυνδέθηκες.")
    return redirect(url_for('student.login'))

@student_bp.route("/create", methods=["GET", "POST"])
def create_questionnaire():
    if request.method == "POST":
        db = get_db()
        title = request.form["title"]
        description = request.form["description"]
        student_id = session.get("reg_number") 

        questions = []
        for i in range(len(request.form.getlist("question_type"))):
            questions.append({
                "type": request.form.getlist("question_type")[i],
                "description": request.form.getlist("question_text")[i],
                "question_num": i + 1
            })

        questionnaire_id = str(uuid4())
        unique_url = f"/questionnaire/view?qid={questionnaire_id}"

        questionnaire = {
            "student_id": student_id,
            "questionnaire_id": questionnaire_id,
            "title": title,
            "description": description,
            "answer_count": 0,
            "unique_url": unique_url,
            "questions": questions
        }

        db["questionnaires"].insert_one(questionnaire)
        return redirect(url_for("student.dashboard"))

    return render_template("create_questionnaire.html")

@student_bp.route("/my-questionnaires")
def my_questionnaires():
    reg_number = session.get("reg_number")

    if not reg_number:
        # Δεν έχει συνδεθεί
        return redirect(url_for("student.login"))

    db = get_db()
    questionnaires = list(db["questionnaires"].find({"student_id": reg_number}))

    return render_template(
        "view_questionnaires.html",
        questionnaires=questionnaires
    )


