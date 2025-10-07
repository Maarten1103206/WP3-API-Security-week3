import json
from app import create_app
from app.models.models import db, Student, Statement, User

app = create_app()


def import_students(path):
    with open(path, encoding='utf-8') as f:
        data = json.load(f)
    for item in data:
        if not Student.query.filter_by(student_number=str(item['student_number'])).first():
            student = Student(
                student_number=str(item['student_number']),
                name=item['student_name'],
                class_name=item['student_class']
            )
            db.session.add(student)
    print(f"{len(data)} studenten geladen.")


def import_statements(path):
    with open(path, encoding='utf-8') as f:
        data = json.load(f)
    for item in data:
        statement_number = item['statement_number']
        choices = item['statement_choices']
        choice1 = choices[0]
        choice2 = choices[1]

        if not Statement.query.filter_by(number=statement_number).first():
            statement = Statement(
                number=statement_number,
                choice1_text=choice1['choice_text'],
                choice1_letter=choice1['choice_result'],
                choice2_text=choice2['choice_text'],
                choice2_letter=choice2['choice_result']
            )
            db.session.add(statement)

    print(f"{len(data)} stellingen geladen.")


with app.app_context():
    db.drop_all()
    db.create_all()

    import_students('students.json')
    import_statements('actiontype_statements.json')

    if not User.query.filter_by(username='admin').first():
        user = User(username='admin', is_admin=True)
        user.set_password('test123')
        db.session.add(user)
        print("Admin gebruiker aangemaakt (admin/test123)")

    db.session.commit()
    print("Data import voltooid.")
