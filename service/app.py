from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///./teams.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)

class Team(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    passed = db.Column(db.Integer, nullable=False)
    failed = db.Column(db.Integer, nullable=False)
    pending = db.Column(db.Integer, nullable=False)
    undefined = db.Column(db.Integer)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

@app.route('/teams')
def get_teams():
    today = datetime.utcnow().date()
    teams = Team.query.filter(db.func.date(Team.date_created) == today).all()
    return jsonify({'teams': [{'name': team.name, 'testResults': {'passed': team.passed, 'failed': team.failed, 'pending': team.pending, 'undefined': team.undefined}} for team in teams]})

if __name__ == '__main__':
    app.run(debug=True)

@app.cli.command('seed_db')
def seed_db():
    """Seeds the database with initial data."""
    teams = [
        Team(name='Team 1', passed=18, failed=2, pending=0, undefined=0),
        Team(name='Team Alpha', passed=10, failed=2, pending=2, undefined=0),
        Team(name='Team B', passed=1, failed=2, pending=1, undefined=0),
        Team(name='Team 4 behave', passed=2, failed=2, pending=0, undefined=2),
        Team(name='Team 5', passed=20, failed=1, pending=1, undefined=0)
    ]
    db.session.bulk_save_objects(teams)
    db.session.commit()

    print('Database seeded!')
