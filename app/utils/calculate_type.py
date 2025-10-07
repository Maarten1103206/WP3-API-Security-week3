from app.models.models import Answer, Statement

def calculate_action_type(student):
    # Haalt alle antwoorden van deze student op
    answers = Answer.query.filter_by(student_id=student.id).all()

    # Counts per letter
    counts = {
        'E': 0, 'I': 0,
        'S': 0, 'N': 0,
        'T': 0, 'F': 0,
        'J': 0, 'P': 0
    }

    for answer in answers:
        statement = answer.statement
        if answer.choice_number == 1:
            letter = statement.choice1_letter
        else:
            letter = statement.choice2_letter
        counts[letter] += 1

    # Bepaalt het type: steeds de hoogste per duo
    result = ''
    result += 'E' if counts['E'] >= counts['I'] else 'I'
    result += 'S' if counts['S'] >= counts['N'] else 'N'
    result += 'T' if counts['T'] >= counts['F'] else 'F'
    result += 'J' if counts['J'] >= counts['P'] else 'P'

    return result
