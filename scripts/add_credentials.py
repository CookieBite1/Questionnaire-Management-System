import json
import sys
import os
from pathlib import Path

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

def extract_username(email):
    return email.split("@")[0]

def main():
    cur_path = os.getcwd()
    INPUT_PATH = Path(cur_path) / 'app' / 'data_files' / 'students.json'
    print(INPUT_PATH)
    with open(INPUT_PATH, "r", encoding="utf-8") as f:
        students = json.load(f)

    for student in students:
        if "email" in student:
            student["username"] = extract_username(student["email"])
            student["password"] = "1234"  # 🔐 Ή βάλε custom logic

    OUTPUT_PATH = Path(cur_path) / 'app' / 'data_files' / 'students_with_credentials.json'
    print(OUTPUT_PATH)
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(students, f, indent=4, ensure_ascii=False)

    print(f"✅ Αποθηκεύτηκε με επιτυχία στο {OUTPUT_PATH}")

if __name__ == "__main__":
    main()
