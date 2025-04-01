import os

class Config(object):
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = 'static/uploads'
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max upload

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///gifts.db'
    SECRET_KEY = 'dev-key'

class ProductionConfig(Config):
    DEBUG = False
    # Use environment variable for production database
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI', 'sqlite:///gifts.db')
    SECRET_KEY = os.environ.get('SECRET_KEY', 'production-secret-key')

# Default to development config
config_by_name = {
    'dev': DevelopmentConfig,
    'prod': ProductionConfig
}
