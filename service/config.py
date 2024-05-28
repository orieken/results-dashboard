class Config:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///./teams.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///./test_teams.db'
