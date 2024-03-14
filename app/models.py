from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from app.db import db
from app import app


class User(db.Model):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String(40), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(40), nullable=False)
    password: Mapped[str] = mapped_column(String(20), nullable=False)

    def to_dict(self):
        return {"user_id": self.id, "username": self.username, "email": self.email}

    @staticmethod
    def is_unique_email(email):
        user = (
            db.session.execute(db.select(User).where(User.email == email))
            .scalars()
            .all()
        )
        return user == []

    @classmethod
    def is_unique_username(cls, username):
        user = (
            db.session.execute(db.select(cls).where(cls.username == username))
            .scalars()
            .all()
        )
        return user == []

    @classmethod
    def is_valid_id(cls, id):
        user = db.session.execute(db.select(cls).where(cls.id == id)).scalars().all()
        return user != []


class Friend(db.Model):
    __tablename__ = "friends"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(40), nullable=False)
    user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.id"), nullable=False
    )
    description: Mapped[str] = mapped_column(String(200))
    count_notes: Mapped[int] = mapped_column(Integer, default=0)
    sum_of_notes: Mapped[int] = mapped_column(Integer, default=0)

    def to_dict(self):
        return {
            "user_id": self.user_id,
            "friend_id": self.id,
            "friend_name": self.name,
            "description": self.description,
            "rating": self.calculate_rating(),
            "notes": self.get_notes(),
        }

    def calculate_rating(self):
        if self.count_notes == 0:
            return "Not enough data"
        return f"{self.sum_of_notes/self.count_notes:.2f}"

    def get_notes(self):
        notes = (
            db.session.execute(
                db.select(Note).where(
                    (Note.user_id == self.user_id) & (Note.friend_id == self.id)
                )
            )
            .scalars()
            .all()
        )
        notes = [note.to_dict() for note in notes]
        return notes

    @classmethod
    def is_valid_id(cls, id):
        friend = db.session.execute(db.select(cls).where(cls.id == id)).scalars().all()
        return friend != []


class Note(db.Model):
    __tablename__ = "notes"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"))
    friend_id: Mapped[int] = mapped_column(Integer, ForeignKey("friends.id"))
    description: Mapped[str] = mapped_column(String(200), nullable=False)
    score: Mapped[int] = mapped_column(Integer, nullable=False)

    def to_dict(self):
        return {
            "note_id": self.id,
            "user_id": self.user_id,
            "friend_id": self.friend_id,
            "description": self.description,
            "score": self.score,
        }

    @staticmethod
    def is_valid_score(score):
        return isinstance(score, int) and int(score) == score and 1 <= score <= 5


with app.app_context():
    db.create_all()
