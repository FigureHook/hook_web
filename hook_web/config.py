import os
from base64 import b64encode
from os import urandom

from redis import Redis


class Config(object):
    """Base config, uses staging database server."""
    DISCORD_CLIENT_ID = os.environ.get("DISCORD_CLIENT_ID")
    DISCORD_CLIENT_SECRET = os.environ.get("DISCORD_CLIENT_SECRET")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SESSION_TYPE = 'redis'
    SESSION_USE_SIGNER = True
    SESSION_REDIS = Redis(
        host=os.environ.get('REDIS_HOST', "127.0.0.1"),
        port=int(os.environ.get('REDIS_PORT', "6379")),
        password=os.environ.get('REDIS_PASSWORD')
    )

    @property
    def SQLALCHEMY_DATABASE_URI(self):
        db_url = os.getenv("POSTGRES_URL")
        db_user = os.getenv('POSTGRES_USER')
        db_pw = os.getenv('POSTGRES_PASSWORD')
        database = os.getenv('POSTGRES_DATABASE')
        return f"postgresql+psycopg2://{db_user}:{db_pw}@{db_url}/{database}"


class ProductionConfig(Config):
    """Uses production database server."""
    SERVER_NAME = os.environ.get("FLASK_SERVER_NAME")
    SECRET_KEY = os.environ.get("FLASK_SECRET_KEY")
    SESSION_COOKIE_SECURE = True
    PERMANENT_SESSION_LIFETIME = 3600


class StagingConfig(Config):
    """Uses production database server."""
    SERVER_NAME = os.environ.get("FLASK_SERVER_NAME")
    SECRET_KEY = os.environ.get("FLASK_SECRET_KEY")
    PERMANENT_SESSION_LIFETIME = 3600


class DevelopmentConfig(Config):
    SECRET_KEY = b64encode(urandom(32)).decode('utf-8')
    SESSION_PERMANENT = False
    TEMPLATES_AUTO_RELOAD = True


class TestingConfig(Config):
    SERVER_NAME = "hook-test.local"
    WTF_CSRF_ENABLED = False
    SECRET_KEY = "test"

    # @property
    # def SQLALCHEMY_DATABASE_URI(self):
    #     db_url = os.getenv("POSTGRES_URL")
    #     db_user = os.getenv('POSTGRES_USER')
    #     db_pw = os.getenv('POSTGRES_PASSWORD')
    #     database = 'figure_testing'
    #     return f"postgresql+psycopg2://{db_user}:{db_pw}@{db_url}/{database}"


config = {
    "production": ProductionConfig,
    "development": DevelopmentConfig,
    "test": TestingConfig,
    "staging": StagingConfig
}
