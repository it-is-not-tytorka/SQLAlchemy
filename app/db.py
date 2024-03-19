from sqlalchemy_utils import database_exists, create_database
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from app import app


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)

# there's a URL of your database. as default, you can use "sqlite:///project.db"
DB_URL = "YOUR DATABASE URL"
app.config["SQLALCHEMY_DATABASE_URI"] = DB_URL
db.init_app(app)

# create database only at the first time
if not database_exists(DB_URL):
    create_database(DB_URL)
