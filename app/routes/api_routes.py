from flask import request, jsonify, Blueprint
from app.models.models import db, Student, Statement, Answer

api_bp = Blueprint('api', __name__, url_prefix='/api')


@api_bp.route('/student/<student_number>/statement', methods=['GET'])
def get_next_statement(student_number):
    # Check of student bestaat
    student = Student.query.filter_by(student_number=student_number).first()
    if not student:
        return jsonify({"error": "Student niet gevonden."}), 404

    # Haalt lijst op van alle beantwoorde statements
    answered_ids = [a.statement_id for a in student.answers]

    # Vind de volgende onbeantwoorde stelling
    next_statement = Statement.query.filter(~Statement.id.in_(answered_ids)) \
        .order_by(Statement.number).first()

    if not next_statement:
        return jsonify({"message": "Alle stellingen zijn al ingevuld."}), 200

    # Maakt response zoals opdracht vereist
    response = {
        "statement_number": next_statement.number,
        "statement_choices": [
            {
                "choice_number": 1,
                "choice_text": next_statement.choice1_text
            },
            {
                "choice_number": 2,
                "choice_text": next_statement.choice2_text
            }
        ]
    }
    return jsonify(response), 200


@api_bp.route('/student/<student_number>/statement/<int:statement_number>', methods=['POST'])
def save_answer(student_number, statement_number):
    data = request.get_json()

    # Checkt of er statement_choice in de body staat
    if not data or 'statement_choice' not in data:
        return jsonify({"error": "Geen keuze ontvangen."}), 400

    choice = data['statement_choice']

    # Student & Stelling ophalen
    student = Student.query.filter_by(student_number=student_number).first()
    statement = Statement.query.filter_by(number=statement_number).first()

    if not student or not statement:
        return jsonify({"error": "Student of stelling niet gevonden."}), 404

    # Checkt of antwoord al bestaat
    existing = Answer.query.filter_by(student_id=student.id, statement_id=statement.id).first()
    if existing:
        return jsonify({"error": "Deze stelling is al beantwoord."}), 400

    # Nieuw antwoord aanmaken
    new_answer = Answer(
        student_id=student.id,
        statement_id=statement.id,
        choice_number=choice
    )

    db.session.add(new_answer)
    db.session.commit()

    return jsonify({"result": "ok"}), 200


@api_bp.route('/student/<student_number>/info', methods=['GET'])
def get_student_info(student_number):
    student = Student.query.filter_by(student_number=student_number).first()
    if not student:
        return jsonify({"error": "Student niet gevonden"}), 404

    return jsonify({
        "name": student.name,
        "class_name": student.class_name
    }), 200


from app.utils.calculate_type import calculate_action_type


@api_bp.route('/student/<student_number>/type', methods=['GET'])
def get_action_type(student_number):
    student = Student.query.filter_by(student_number=student_number).first()
    if not student:
        return jsonify({"error": "Student niet gevonden"}), 404

    answers = Answer.query.filter_by(student_id=student.id).all()
    if len(answers) < 20:
        return jsonify({"error": "Niet genoeg antwoorden om type te bepalen."}), 400

    action_type = calculate_action_type(student)
    return jsonify({"action_type": action_type})
