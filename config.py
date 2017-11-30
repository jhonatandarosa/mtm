# Define the application directory
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    DEBUG = False
    TESTING = False
    # Enable protection agains *Cross-site Request Forgery (CSRF)*
    CSRF_ENABLED = True
    # Use a secure, unique and absolutely secret key for
    # signing the data.
    CSRF_SESSION_KEY = "secret"
    # Secret key for signing cookies
    SECRET_KEY = 'secret'
    # Define the database - we are working with
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    # If set to True, Flask-SQLAlchemy will track modifications of objects and emit signals. This requires extra memory and should be disabled if not needed.
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProductionConfig(Config):
    DEBUG = False


class StagingConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class TestingConfig(Config):
    TESTING = True
