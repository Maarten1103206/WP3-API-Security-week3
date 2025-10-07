from flask import Blueprint, render_template

student_bp = Blueprint('student', __name__)


@student_bp.route('/')
def index():
    return render_template('index.html')


@student_bp.route('/vragenlijst')
def vragenlijst():
    return render_template('questions.html')
