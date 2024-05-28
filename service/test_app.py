import pytest
from flask_testing import TestCase
from app import app, db, Team

class MyTest(TestCase):
    def create_app(self):
        app.config.from_object('config.TestConfig')
        return app

    def setUp(self):
        db.create_all()
        db.session.add(Team(name='Test Team', passed=10, failed=1, pending=2, undefined=0))
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_get_teams(self):
        response = self.client.get('/teams')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Test Team', response.json['teams'][0]['name'])
        self.assertEqual(response.json['teams'][0]['testResults']['passed'], 10)
