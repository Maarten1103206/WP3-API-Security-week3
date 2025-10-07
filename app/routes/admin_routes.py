from flask import Blueprint, render_template, request, redirect, session, url_for, request, make_response
from app.models.models import User, Student, Answer, db
from app.utils.calculate_type import calculate_action_type
from sqlalchemy import func
from datetime import datetime
import csv

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')


@admin_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            session['logged_in'] = True
            session['username'] = user.username
            return redirect(url_for('admin.dashboard'))

        return render_template('admin_login.html', error="Ongeldige inloggegevens")

    return render_template('admin_login.html')


@admin_bp.route('/add_student', methods=['POST'])
def add_student():
    if not session.get('logged_in'):
        return redirect(url_for('admin.login'))

    student_number = request.form['student_number']
    name = request.form['name']
    klas = request.form['class']

    if Student.query.filter_by(student_number=student_number).first():
        return "Student bestaat al!", 400

    new_student = Student(student_number=student_number, name=name, class_name=klas)
    db.session.add(new_student)
    db.session.commit()
    return redirect(url_for('admin.dashboard'))


@admin_bp.route('/student/<student_number>')
def student_details(student_number):
    if not session.get('logged_in'):
        return redirect(url_for('admin.login'))

    student = Student.query.filter_by(student_number=student_number).first_or_404()
    answers = Answer.query.filter_by(student_id=student.id).all()
    return render_template('student_details.html', student=student, answers=answers)


@admin_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('admin.login'))


@admin_bp.route('/')
def dashboard():
    if not session.get('logged_in'):
        return redirect(url_for('admin.login'))

    students = Student.query.all()
    data = []
    for student in students:
        answers = Answer.query.filter_by(student_id=student.id).order_by(Answer.timestamp.desc()).all()
        last_date = answers[0].timestamp.strftime('%d-%m-%Y %H:%M') if answers else None
        action_type = calculate_action_type(student) if len(answers) == 20 else "?"

        data.append({
            "student_number": student.student_number,
            "name": student.name,
            "class": student.class_name,
            "last_answer_date": last_date,
            "action_type": action_type
        })

    return render_template('dashboard.html', students=data)


@admin_bp.route('/add_student', methods=['POST'])
def add_student_view():
    if not session.get('logged_in'):
        return redirect(url_for('admin.login'))

    student_number = request.form['student_number']
    name = request.form['name']
    klas = request.form['class']

    if Student.query.filter_by(student_number=student_number).first():
        return "Student bestaat al!", 400

    new_student = Student(student_number=student_number, name=name, class_name=klas)
    db.session.add(new_student)
    db.session.commit()
    return redirect(url_for('admin.dashboard'))


@admin_bp.route('/delete/<student_number>', methods=['POST'])
def delete_student(student_number):
    if not session.get('logged_in'):
        return redirect(url_for('admin.login'))

    student = Student.query.filter_by(student_number=student_number).first()
    if student:
        db.session.delete(student)
        db.session.commit()
    return redirect(url_for('admin.dashboard'))


@admin_bp.route('/export')
def export_students():
    if not session.get('logged_in'):
        return redirect(url_for('admin.login'))

    students = Student.query.all()

    output = []
    output.append(['Studentnummer', 'Naam', 'Actiontype', 'Datum laatste antwoord', 'Klas', 'Team'])

    for student in students:
        last_answer = (
            Answer.query
            .filter_by(student_id=student.id)
            .order_by(Answer.timestamp.desc())
            .first()
        )
        action_type = calculate_action_type(student) if student.answers else ''
        last_date = last_answer.timestamp.strftime("%Y-%m-%d %H:%M") if last_answer else ''
        output.append([
            student.student_number,
            student.name,
            action_type,
            last_date,
            student.class_name,
            student.team or ''
        ])

    # CSV response gen
    si = csv.StringIO()
    writer = csv.writer(si)
    writer.writerows(output)

    response = make_response(si.getvalue())
    response.headers['Content-Disposition'] = 'attachment; filename=student_export.csv'
    response.headers['Content-type'] = 'text/csv'
    return response
