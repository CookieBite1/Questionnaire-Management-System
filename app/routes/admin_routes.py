from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from app.models.student_model import create_student, delete_student_by_reg_number
from app.models.student_model import get_all_students
from app.models.questionnaire_model import get_all_questionnaires_sorted
from app.models.questionnaire_model import search_questionnaires
from app.db.db_operations import get_db

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == 'admin' and password == 'admin123':
            session['admin'] = True
            flash("Καλωσήρθες διαχειριστή!", "success")
            return redirect(url_for('admin.manage_students'))
        else:
            flash("Λάθος στοιχεία!", "error")
    return render_template('admin_login.html')

@admin_bp.route('/manage-students')
def manage_students():
    if not session.get('admin'):
        return redirect(url_for('admin.admin_login'))
    students = get_all_students()
    print(students)
    return render_template('manage_students.html', students=students)

@admin_bp.route('/create-student', methods=['GET', 'POST'])
def create_student_view():
    if request.method == 'POST':
        data = {
            "username": request.form['username'],
            "password": request.form['password'],
            "reg_number": int(request.form['reg_number']),
            "department": request.form['department'],
            "name": request.form['name'],
            "surname": request.form['surname']
        }
        create_student(data)
        return redirect('/admin/manage-students')
    return render_template('create_student.html')

@admin_bp.route('/delete-student/<reg_number>')
def delete_student_view(reg_number):
    delete_student_by_reg_number(int(reg_number))
    return redirect('/admin/manage-students')

@admin_bp.route('/questionnaires')
def admin_questionnaires():
    filters = {
        'title': request.args.get('title', ''),
        'min_answers': request.args.get('min_answers', ''),
        'max_answers': request.args.get('max_answers', ''),
        'student_name': request.args.get('student_name', ''),
        'department': request.args.get('department', '')
    }

    sort = request.args.get('sort', '')  # optional

    if any(filters.values()):
        questionnaires = search_questionnaires(filters)
    elif sort:
        questionnaires = get_all_questionnaires_sorted(sort)
    else:
        questionnaires = get_all_questionnaires_sorted('desc')  # default

    return render_template(
        'admin_questionnaires.html',
        questionnaires=questionnaires,
        filters=filters,
        current_sort=sort
    )

@admin_bp.route("/admin/create-student", methods=["GET", "POST"])
def create_student():
    if request.method == "POST":
        student = {
            "name": request.form["name"],
            "surname": request.form["surname"],
            "reg_number": request.form["reg_number"],
            "department": request.form["department"],
            "username": request.form["username"],
            "password": request.form["password"],
        }
        db = get_db()
        if db.students.find_one({"reg_number": student["reg_number"]}):
            flash("Ο φοιτητής υπάρχει ήδη!", "error")
        else:
            db.students.insert_one(student)
            flash("Ο φοιτητής προστέθηκε!", "success")
            return redirect(url_for("admin.manage_students"))

    return render_template("create_student.html")

@admin_bp.route("/admin/delete-student/<reg_number>", methods=["POST"])
def delete_student(reg_number):
    db = get_db()
    db.students.delete_one({"reg_number": reg_number})
    db.questionnaires.delete_many({"student_id": reg_number})
    db.answered_questionnaires.delete_many({"questionnaire_id": {"$in": [
        q["questionnaire_id"] for q in db.questionnaires.find({"student_id": reg_number})
    ]}})
    flash("Ο φοιτητής διαγράφηκε!", "success")
    return redirect(url_for("admin.manage_students"))
