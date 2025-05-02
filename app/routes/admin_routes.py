from flask import Blueprint, render_template, request, redirect
from app.models.student_model import create_student, delete_student_by_reg_number
from app.models.student_model import get_all_students

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/manage-students')
def manage_students():
    students = get_all_students()
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
