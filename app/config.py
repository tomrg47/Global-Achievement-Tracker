import os
from dotenv import load_dotenv

load_dotenv()

class BaseConfig:
    SECRET_KEY = os.getenv("SECRET_KEY")
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(BaseConfig):
    DEBUG = True
    # SQLALCHEMY_DATABASE_URI = "sqlite:///dev.db"
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")


class ProductionConfig(BaseConfig):
    DEBUG = False
    # SQLALCHEMY_DATABASE_URI = "postgresql+pg8000://user:password@host/dbname"
    # if os.getenv("GAE_ENV", "").startswith("standard"):
    #     INSTANCE_CONNECTION_NAME = os.getenv("INSTANCE_CONNECTION_NAME")
    #     DB_USER = os.getenv("DB_USER")
    #     DB_PASS = os.getenv("DB_PASS")
    #     DB_NAME = os.getenv("DB_NAME")

    #     SQLALCHEMY_DATABASE_URI = (
    #         f"postgresql+psycopg2://{DB_USER}:{DB_PASS}"
    #         f"@/cloudsql/{INSTANCE_CONNECTION_NAME}/{DB_NAME}"
    #     )
