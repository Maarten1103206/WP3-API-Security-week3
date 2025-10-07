from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from app.models.models import db
from app.routes.api_routes import api_bp
from app.routes.student_routes import student_bp
from app.routes.admin_routes import admin_bp
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt  # of via init_app in app factory
def create_app():
    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///actiontypes.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'supersecretkey123'

    db.init_app(app)

    app.register_blueprint(api_bp)
    app.register_blueprint(student_bp)
    app.register_blueprint(admin_bp)

    return app  #
