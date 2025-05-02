from app import mongo

# Βρες φοιτητή βάση username
def find_student(username):
    return mongo.db.students.find_one({"username": username})

# Δημιούργησε νέο φοιτητή
def create_student(student_data):
    mongo.db.students.insert_one(student_data)

# Διάγραψε φοιτητή με βάση το registration number
def delete_student_by_reg_number(reg_number):
    mongo.db.students.delete_one({"reg_number": reg_number})

# Βρες όλους τους φοιτητές
def get_all_students():
    return list(mongo.db.students.find())
