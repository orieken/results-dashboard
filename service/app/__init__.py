# from flask import Flask
# from .models import db
#
#
# def create_app(test_config=None):
#     app = Flask(__name__, instance_relative_config=True)
#     app.config.from_mapping(
#         DATABASE="sqlite:///:memory:" if app.config['TESTING'] else "sqlite:///:memory:"
#     )
#
#     db.init_app(app)
#
#     @app.route('/')
#     def hello():
#         return 'Hello, World!'
#
#     return app

from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os

from .models import db, Team, TeamResult
from .routes import configure_routes

migrate = Migrate()


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    CORS(app)
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config.setdefault('SQLALCHEMY_DATABASE_URI', 'sqlite:///your_database.db')

    if test_config:
        app.config.update(test_config)

    db.init_app(app)
    migrate.init_app(app, db)
    configure_routes(app)

    with app.app_context():
        db.create_all()

    return app
