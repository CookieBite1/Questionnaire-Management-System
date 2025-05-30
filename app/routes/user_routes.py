from flask import Blueprint, render_template, request
from flask import request, redirect, url_for, flash
from app.db.db_operations import get_db

user_bp = Blueprint("user", __name__, url_prefix="/user")

@user_bp.route("/questionnaires")
def available_questionnaires():
    db = get_db()

    # Ανάκτηση παραμέτρων φιλτραρίσματος
    min_answers = request.args.get("min_answers", type=int)
    max_answers = request.args.get("max_answers", type=int)
    title = request.args.get("title", "").strip()
    student_name = request.args.get("student_name", "").strip()
    department = request.args.get("department", "").strip()
    sort_order = request.args.get("sort", "desc")

    query = {}

    if title:
        query["title"] = {"$regex": title, "$options": "i"}
    if min_answers is not None or max_answers is not None:
        query["answer_count"] = {}
        if min_answers is not None:
            query["answer_count"]["$gte"] = min_answers
        if max_answers is not None:
            query["answer_count"]["$lte"] = max_answers
    if student_name:
        query["student_name"] = {"$regex": student_name, "$options": "i"}
    if department:
        query["department"] = {"$regex": department, "$options": "i"}

    sort_by = [("answer_count", -1 if sort_order == "desc" else 1)]

    questionnaires = list(db["questionnaires"].find(query).sort(sort_by))

    return render_template("user_questionnaires.html", questionnaires=questionnaires)

@user_bp.route("/questionnaire/<questionnaire_id>", methods=["GET", "POST"])
def view_questionnaire(questionnaire_id):
    db = get_db()
    questionnaire = db["questionnaires"].find_one({"questionnaire_id": questionnaire_id})
    
    if not questionnaire:
        flash("Το ερωτηματολόγιο δεν βρέθηκε.", "error")
        return redirect(url_for("user.available_questionnaires"))

    if request.method == "POST":
        answers = []
        for q in questionnaire.get("questions", []):
            question_num = q["question_num"]
            key = f"q{question_num}"
            content = request.form.get(key)
            if q["type"] == "Numeric":
                try:
                    content = float(content)
                except ValueError:
                    flash(f"Μη έγκυρη αριθμητική τιμή στην ερώτηση {question_num}.", "error")
                    return redirect(request.url)
            answers.append({
                "question_num": question_num,
                "content": content
            })

        db["answered_questionnaires"].insert_one({
            "questionnaire_id": questionnaire_id,
            "from_student": False,
            "answers": answers
        })

        db["questionnaires"].update_one(
            {"questionnaire_id": questionnaire_id},
            {"$inc": {"answer_count": 1}}
        )

        flash("Η απάντηση υποβλήθηκε με επιτυχία!", "success")
        return redirect(url_for("user.available_questionnaires"))

    return render_template("user_answer_questionnaire.html", questionnaire=questionnaire)
