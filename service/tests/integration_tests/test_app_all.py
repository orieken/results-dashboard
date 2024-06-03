import pytest
from app import create_app, db


@pytest.fixture(scope='session')
def test_app():
    config = {
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:',
        'SQLALCHEMY_TRACK_MODIFICATIONS': False
    }
    app = create_app(config)
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(test_app):
    return test_app.test_client()


@pytest.mark.integration
def test_post_results_and_get_history(client):
    # Create a new team
    team_name = "Dynamic Duo"
    response = client.post('/teams', json={
        "name": team_name,
        "results": {
            "passing": 10,
            "failing": 2,
            "pending": 1
        }
    })
    assert response.status_code == 201

    # Update the team with new results
    response = client.post('/teams', json={
        "name": team_name,
        "results": {
            "passing": 12,
            "failing": 1,
            "pending": 3
        }
    })
    assert response.status_code == 201

    # Retrieve all history for the team
    response = client.get(f'/teams/{team_name}/all')
    assert response.status_code == 200
    data = response.get_json()
    assert data['name'] == team_name
    assert 'history' in data
    assert len(data['history']) == 2
    assert data['history'][1]['passing'] == 12