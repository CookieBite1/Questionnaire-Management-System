# Questionnaire-Management-System

# 📅 ΧΡΟΝΙΚΟ ΠΛΑΝΟ (Gantt Plan)
![Instapen](https://github.com/user-attachments/assets/4756005a-744f-432a-8ce7-a1db4893a9a6)

---

# Πίνακας Ρίσκων Υλοποίησης
| Κωδικός | Περιγραφή Ρίσκου                            | Πιθανότητα | Επίδραση | Αντιμετώπιση                                  |
| ------- | ------------------------------------------- | ---------- | -------- | --------------------------------------------- |
| R1      | Αποτυχία σύνδεσης με MongoDB                | Υψηλή      | Υψηλή    | Έλεγχος docker-compose                        |
| R2      | Καθυστέρηση στην είσοδο των φοιτητών        | Μεσαία     | Μεσαία   | Δημιουργία script για προκαθορισμένα accounts |
| R3      | Χρήστες απαντούν λανθασμένα (κακή εμπειρία) | Μεσαία     | Χαμηλή   | Φιλικό UI/UX και επικυρώσεις                  |
| R4      | Απώλεια δεδομένων                           | Χαμηλή     | Υψηλή    | Backup/Restore και logging                    |
| R5      | Παραβίαση ασφάλειας (login/admin access)    | Μεσαία     | Υψηλή    | Hash κωδικών, session controls                |

---

#  📈 Flow Diagram (Data Flow)
[Φοιτητής] --> (Είσοδος στο Σύστημα)
[Χρήστης] --> (Απάντηση Ερωτηματολογίου)
[Διαχειριστής] --> (Διαχείριση Φοιτητών)

(Είσοδος στο Σύστημα) --> [Βάση Δεδομένων]
(Δημιουργία Ερωτηματολογίου) --> [Βάση Δεδομένων]
(Προβολή Ερωτηματολογίου) --> [Βάση Δεδομένων] --> (Αποστολή Δεδομένων)
(Απάντηση Ερωτηματολογίου) --> [Βάση Δεδομένων]

[Βάση Δεδομένων] --> (Προβολή Στατιστικών / Αναφορών)

## Περιεχόμενα
- [Περιγραφή](#περιγραφή)
- [Τεχνολογίες](#τεχνολογίες)
- [Αρχιτεκτονική & Βάση Δεδομένων](#αρχιτεκτονική-βάση-δεδομένων)
- [Οδηγίες Εκτέλεσης](#οδηγίες-εκτέλεσης)
- [Οδηγίες Χρήσης](#οδηγίες-χρήσης)
- [Επιπλέον Παραδοχές](#επιπλέον-παραδοχές)
- [Αναφορές](#αναφορές)

## Περιγραφή
Σύστημα Διαχείρισης, Δημιουργίας, Αναζήτησης και Συμπλήρωσης Ερωτηματολογίων για φοιτητές και χρήστες του Πανεπιστημίου Πειραιώς.

## Τεχνολογίες
- Python 3.11
- Flask (API + Templates)
- MongoDB
- Docker + Docker Compose
- HTML / Bootstrap (για Templates)

## Αρχιτεκτονική & Βάση Δεδομένων
Η βάση δεδομένων περιλαμβάνει 3 collections:
- `students`
- `questionnaires`
- `answered_questionnaires`

**Παράδειγμα εγγραφής:**
```json
{
  "student_id": 12345,
  "questionnaire_id": 67890,
  "title": "Ερωτηματολόγιο για Τεχνητή Νοημοσύνη",
  "description": "Μελέτη για τη χρήση AI στους φοιτητές",
  "answer_count": 0,
  "unique_url": "http://localhost:5000/questionnaire/67890",
  "questions": [
    {
      "type": "Open Ended",
      "description": "Ποια η άποψή σας για την AI;",
      "question_num": 1
    }
  ]
}
```
---

# 🛠️ ΒΗΜΑΤΑ ΥΛΟΠΟΙΗΣΗΣ

## 1. Ανάπτυξη backend API:
- Flask Server
- Endpoints για Users, Students, Admin
- Flask Templates για τα HTML Forms & Lists

## 2. Σύνδεση με MongoDB:
- Μοντέλα για Students, Questionnaires, Answers
- Χρήση `pymongo`

## 3. Δημιουργία UI:
- Flask Templates για:
  - Εμφάνιση Ερωτηματολογίων
  - Φόρμες Απαντήσεων
  - CRUD Ερωτηματολογίων για Students

## 4. Dockerization:
- Γραφή `Dockerfile`
- Γραφή `docker-compose.yaml`:
  - Flask app container
  - MongoDB container με mounted volume `/data`

## 5. Αρχικοποίηση DB:
- Εισαγωγή των `students.json`, `questionnaires.json`, `answered_questionnaires.json`
- Δημιουργία Admin account

## 6. Τεκμηρίωση:
- README.md
- Gantt Chart
- Data Flow Diagram
- Risk Table
---
```
project/
├── app/
│   ├── __init__.py
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── user_routes.py
│   │   ├── student_routes.py
│   │   ├── admin_routes.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── student_model.py
│   │   ├── questionnaire_model.py
│   │   ├── answered_model.py
│   ├── templates/
│   │   ├── base.html
│   │   ├── index.html
│   │   ├── login.html
│   │   ├── view_questionnaires.html
│   │   ├── answer_questionnaire.html
│   │   └── create_questionnaire.html
│   └── static/
│       └── (css/js αν χρειαστεί)
├── data/
│   ├── students.json
│   ├── questionnaires.json
│   ├── answered_questionnaires.json
├── Dockerfile
├── docker-compose.yaml
├── requirements.txt
├── README.md
└── run.py
```
