import sys
import os
from pathlib import Path

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app
from app.db.db_operations import load_collection

app = create_app()

if __name__ == '__main__':
    cur_path = os.getcwd()
    working_dir = Path(cur_path).parent / 'app' / 'data_files'
    print(working_dir)
    with app.app_context():
        students_path = working_dir / 'students.json'
        load_collection(students_path, 'students')

        questionnaires_path = working_dir / 'questionnaires.json'
        load_collection(questionnaires_path, 'questionnaires')

        answered_questionnaires_path = working_dir / 'answered_questionnaires.json'
        load_collection(answered_questionnaires_path, 'answered_questionnaires')
