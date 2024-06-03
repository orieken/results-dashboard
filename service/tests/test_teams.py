import pytest
from app import create_app, db
from app.models import Team


@pytest.fixture
def client():
    app = create_app({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:'
    })
    with app.app_context():
        db.create_all()
        yield app.test_client()
        db.session.remove()
        db.drop_all()


@pytest.mark.unit
def test_create_team_valid(client):
    """Test creating a team with valid data."""
    data = {
        "name": "Team 1",
        "results": {
            "passing": 10,
            "failing": 2,
            "pending": 5
        }
    }
    response = client.post('/teams', json=data)
    assert response.status_code == 201
    assert response.json == {"message": "Team created successfully"}
    # Check if team was actually inserted into the database
    with client.application.app_context():
        team = Team.query.first()
        assert team is not None
        assert team.name == "Team 1"
        assert team.passing == 10
        assert team.failing == 2
        assert team.pending == 5


@pytest.mark.unit
def test_create_team_invalid(client):
    """Test creating a team with invalid data."""
    data = {
        "name": "Team 2",
        "results": {
            "passing": 15
            # Missing 'failing' and 'pending'
        }
    }
    response = client.post('/teams', json=data)
    assert response.status_code == 400
    assert "error" in response.json
    # Ensure database is still empty
    with client.application.app_context():
        count = Team.query.count()
        assert count == 0
