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

@student_bp.route('/edit-questionnaire/<questionnaire_id>', methods=['GET', 'POST'])
def edit_questionnaire(questionnaire_id):
    db = get_db()
    questionnaire = db['questionnaires'].find_one({"questionnaire_id": questionnaire_id})

    if not questionnaire:
        flash("Δεν βρέθηκε το ερωτηματολόγιο.", "error")
        return redirect(url_for("student.my_questionnaires"))

    if request.method == 'POST':
        new_title = request.form['title']
        db['questionnaires'].update_one(
            {"questionnaire_id": questionnaire_id},
            {"$set": {"title": new_title}}
        )
        flash("Ο τίτλος ενημερώθηκε!", "success")
        return redirect(url_for("student.my_questionnaires"))

    return render_template('edit_questionnaire.html', questionnaire=questionnaire)

@student_bp.route('/delete-questionnaire/<questionnaire_id>', methods=['POST'])
def delete_questionnaire(questionnaire_id):
    db = get_db()
    db['questionnaires'].delete_one({"questionnaire_id": questionnaire_id})
    db['answered_questionnaires'].delete_many({"questionnaire_id": questionnaire_id})
    flash("Το ερωτηματολόγιο διαγράφηκε.", "success")
    return redirect(url_for('student.my_questionnaires'))

@student_bp.route("/questionnaire/<questionnaire_id>/answers", methods=["GET"])
def questionnaire_answers(questionnaire_id):
    db = get_db()

    # Βρες το ερωτηματολόγιο
    questionnaire = db["questionnaires"].find_one({"questionnaire_id": questionnaire_id})
    if not questionnaire:
        flash("Το ερωτηματολόγιο δεν βρέθηκε.", "error")
        return redirect(url_for("student.my_questionnaires"))

    # Βρες τις απαντήσεις
    answers = list(db["answered_questionnaires"].find({"questionnaire_id": questionnaire_id}))

    total = len(answers)
    from_student = len([a for a in answers if a.get("from_student")])
    from_user = total - from_student
    user_percentage = round((from_user / total) * 100, 2) if total > 0 else 0

    return render_template(
        "questionnaire_answers.html",
        questionnaire=questionnaire,
        answers=answers,
        total=total,
        from_student=from_student,
        from_user=from_user,
        user_percentage=user_percentage
    )

# app/routes/student_routes.py
@student_bp.route('/change-password', methods=['GET', 'POST'])
def change_password():
    if 'student' not in session:
        return redirect(url_for('student.login'))

    db = get_db()
    username = session['student']
    student = db.students.find_one({'username': username})

    if request.method == 'POST':
        current = request.form['current_password']
        new = request.form['new_password']
        confirm = request.form['confirm_password']

        if student['password'] != current:
            flash('Ο τρέχων κωδικός είναι λάθος.', 'error')
        elif new != confirm:
            flash('Οι νέοι κωδικοί δεν ταιριάζουν.', 'error')
        else:
            db.students.update_one({'username': username}, {'$set': {'password': new}})
            flash('Ο κωδικός άλλαξε με επιτυχία.', 'success')
            return redirect(url_for('student.dashboard'))

    return render_template('change_password.html')
