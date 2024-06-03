import pytest
from datetime import datetime
from flask import url_for
from app import create_app, db
from app.models import Team, TeamResult


@pytest.fixture
def client():
    """Fixture to create a Flask test client and setup/teardown test database."""
    app = create_app({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:',
        'SERVER_NAME': 'localhost.localdomain'
        })
    with app.app_context():
        db.create_all()
        yield app.test_client()  # provides a test client for the Flask app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def sample_team():
    """Fixture to insert sample team and results into the database."""
    team = Team(name='Test Team', last_updated=datetime.utcnow())
    db.session.add(team)
    db.session.add(TeamResult(team=team, passing=10, failing=3, pending=7, created_at=datetime.utcnow()))
    db.session.add(TeamResult(team=team, passing=12, failing=1, pending=9, created_at=datetime.utcnow()))
    db.session.commit()
    return team


@pytest.mark.unit
def test_get_all_team_results(client, sample_team):
    """Test fetching all results for a specific team."""
    response = client.get(url_for('get_all_team_results', team_name=sample_team.name))
    assert response.status_code == 200
    data = response.get_json()
    assert data['name'] == 'Test Team'
    assert len(data['history']) == 2  # Ensure history contains 2 records
    assert data['latest_results']['passing'] == 12  # Check the latest result data


@pytest.mark.unit
def test_get_all_team_results_no_team(client):
    """Test response for a non-existent team."""
    response = client.get(url_for('get_all_team_results', team_name='Nonexistent Team'))
    assert response.status_code == 404
    data = response.get_json()
    assert data['message'] == 'Team not found'
