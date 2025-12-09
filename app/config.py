class BaseConfig:
    SECRET_KEY = "your-secret-key"
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(BaseConfig):
    DEBUG = True
    # SQLALCHEMY_DATABASE_URI = "sqlite:///dev.db"


class ProductionConfig(BaseConfig):
    DEBUG = False
    # SQLALCHEMY_DATABASE_URI = "postgresql+pg8000://user:password@host/dbname"
