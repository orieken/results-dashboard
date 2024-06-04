# import pytest
# from unittest.mock import Mock
# from flask import url_for
# from app import create_app, db
# from app.models import Team
#
#
# @pytest.fixture
# def client():
#     app = create_app({
#         'TESTING': True,
#         'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:',
#         'SERVER_NAME': 'localhost.localdomain'
#     })
#     with app.app_context():
#         db.create_all()
#         yield app.test_client()
#         db.session.remove()
#         db.drop_all()
#
#
# @pytest.fixture
# def mock_query(monkeypatch):
#     mock = Mock()
#     monkeypatch.setattr(db.session, 'query', mock)
#     return mock
#
#
# @pytest.mark.unit
# def test_team_summary_valid_data(client, mock_query):
#     # Setup mock return values for aggregate and individual queries
#     mock_result_aggregate = Mock()
#     mock_result_aggregate.total_passing = 25
#     mock_result_aggregate.total_failing = 3
#     mock_result_aggregate.total_pending = 17
#     mock_query().add_columns(Mock()).one.return_value = mock_result_aggregate
#
#     mock_query().add_columns(Mock()).all.return_value = [
#         {'Team': {'name': 'Team 1', 'passing': 12, 'failing': 1, 'pending': 8}},
#         {'Team': {'name': 'Team 2', 'passing': 13, 'failing': 2, 'pending': 9}}
#     ]
#
#     response = client.get(url_for('get_team_summaries'))
#     assert response.status_code == 200
#     json_data = response.get_json()
#     assert json_data == {
#         "summary": {"passing": 25, "failing": 3, "pending": 17},
#         "teams": [
#             {"name": "Team 1", "totals": {"passing": 12, "failing": 1, "pending": 8}},
#             {"name": "Team 2", "totals": {"passing": 13, "failing": 2, "pending": 9}}
#         ]
#     }
#
#
#
# # @pytest.mark.unit
# # def test_team_summary_no_data(client, mock_query):
# #     # Setup mock to return no data
# #     mock_result_aggregate = Mock()
# #     mock_result_aggregate.total_passing = 0
# #     mock_result_aggregate.total_failing = 0
# #     mock_result_aggregate.total_pending = 0
# #     mock_query.return_value.one.return_value = mock_result_aggregate
# #
# #     mock_query.return_value.all.return_value = []
# #
# #     response = client.get(url_for('get_team_summaries'))
# #     assert response.status_code == 200
# #     json_data = response.get_json()
# #     assert json_data == {
# #         "summary": {"passing": 0, "failing": 0, "pending": 0},
# #         "teams": []
# #     }

import pytest
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_testing import TestCase
from unittest.mock import patch
from app.models import db

def create_app():
    app = Flask(__name__)
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'  # Use in-memory SQLite database for testing
    db.init_app(app)
    return app


class BaseTestCase(TestCase):
    def create_app(self):
        return create_app()

    def setUp(self):
        self.client = self.app.test_client()
        with self.app.app_context():
            db.create_all()  # Set up a blank temporary database

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()  # Clear the temporary database


class TestTeamSummary(BaseTestCase):

    @pytest.mark.unit
    @patch('app.models.db')
    def test_team_summary_valid_data(self, mock_db):
        mock_db.session.query().add_columns().all.return_value = [
            {'Team': {'name': 'Team 1', 'passing': 20, 'failing': 5, 'pending': 3}},
            {'Team': {'name': 'Team 2', 'passing': 15, 'failing': 7, 'pending': 12}}
        ]
        mock_db.session.query().one.return_value = {
            'total_passing': 35,
            'total_failing': 12,
            'total_pending': 15
        }

        response = self.client.get('/teams/summary')

        self.assert200(response)
        self.assertEqual(
            response.get_json(),
            {
                'summary': {'passing': 35, 'failing': 12, 'pending': 15},
                'teams': [
                    {'name': 'Team 1', 'totals': {'passing': 20, 'failing': 5, 'pending': 3}},
                    {'name': 'Team 2', 'totals': {'passing': 15, 'failing': 7, 'pending': 12}}
                ]
            }
        )

    @pytest.mark.unit
    @patch('app.models.db')
    def test_team_summary_no_data(self, mock_db):
        mock_db.session.query().add_columns().all.return_value = []
        mock_db.session.query().one.return_value = {
            'total_passing': 0,
            'total_failing': 0,
            'total_pending': 0
        }

        response = self.client.get('/teams/summary')

        self.assert200(response)
        self.assertEqual(
            response.get_json(),
            {
                'summary': {'passing': 0, 'failing': 0, 'pending': 0},
                'teams': []
            }
        )