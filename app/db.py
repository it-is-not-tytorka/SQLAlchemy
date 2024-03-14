import os
from dotenv import load_dotenv
from sqlalchemy_utils import database_exists, create_database
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from app import app

load_dotenv()


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)


DB_URL = f'postgresql+psycopg://{os.getenv('DB_USER_NAME')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}'
app.config["SQLALCHEMY_DATABASE_URI"] = DB_URL
db.init_app(app)

if not database_exists(DB_URL):
    create_database(DB_URL)
