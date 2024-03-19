from app.db import db
from app import app
from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column


class User(db.Model):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String(40), nullable=False)
    email: Mapped[str] = mapped_column(String(40), nullable=False)
    password: Mapped[str] = mapped_column(String(20), nullable=False)

    def to_dict(self) -> dict:
        return {
            "user_id": self.id,
            "username": self.username,
            "email": self.email,
            "password": self.password,
        }

    @staticmethod
    def is_unique_email(email: str) -> bool:
        user = (
            db.session.execute(db.select(User).where(User.email == email))
            .scalars()
            .all()
        )
        return user == []

    @classmethod
    def is_valid_id(cls, user_id: int) -> bool:
        user = (
            db.session.execute(db.select(cls).where(cls.id == user_id)).scalars().all()
        )
        return user != []


class Friend(db.Model):
    __tablename__ = "friends"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.id"), nullable=False
    )
    name: Mapped[str] = mapped_column(String(40), nullable=False)
    description: Mapped[str] = mapped_column(String(200))
    count_notes: Mapped[int] = mapped_column(Integer, default=0)
    sum_of_notes: Mapped[int] = mapped_column(Integer, default=0)
    # if deleted = 0 then a friend isn't deleted
    # if deleted = 1 then a friend is deleted, and we can't see him running /friend, /friend/all
    # or edit him running /friend/edit
    deleted: Mapped[int] = mapped_column(Integer, default=0)

    def to_dict(self) -> dict:
        return {
            "user_id": self.user_id,
            "friend_id": self.id,
            "friend_name": self.name,
            "description": self.description,
            "rating": self.calculate_rating(self.id),
            "notes": self.get_notes(),
        }

    @classmethod
    def calculate_rating(cls, friend_id: int) -> str:
        friend = (
            db.session.execute(db.select(cls).where(cls.id == friend_id))
            .scalars()
            .all()[0]
        )
        if friend.count_notes == 0:
            return "Not enough data"
        return f"{friend.sum_of_notes/friend.count_notes:.2f}"

    def get_notes(self) -> list[dict]:
        notes = (
            db.session.execute(
                db.select(Note).where((Note.friend_id == self.id) & (Note.deleted == 0))
            )
            .scalars()
            .all()
        )
        notes = [note.to_dict() for note in notes]
        return notes

    def remove(self) -> None:
        self.deleted = 1

    def restore(self) -> None:
        self.deleted = 0

    @classmethod
    def change_sum_of_notes(cls, friend_id: int, value: int | float) -> None:
        friend = (
            db.session.execute(db.select(cls).where(cls.id == friend_id))
            .scalars()
            .all()[0]
        )
        friend.sum_of_notes += value

    @classmethod
    def change_count_notes(cls, friend_id: int, value: int) -> None:
        friend = (
            db.session.execute(db.select(cls).where(cls.id == friend_id))
            .scalars()
            .all()[0]
        )
        friend.count_notes += value

    @classmethod
    def is_valid_id(cls, friend_id: int) -> bool:
        friend = (
            db.session.execute(db.select(cls).where(cls.id == friend_id))
            .scalars()
            .all()
        )
        return friend != []


class Note(db.Model):
    __tablename__ = "notes"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"))
    friend_id: Mapped[int] = mapped_column(Integer, ForeignKey("friends.id"))
    description: Mapped[str] = mapped_column(String(200), nullable=False)
    score: Mapped[int] = mapped_column(Integer, nullable=False)
    # if deleted = 0 then a note isn't deleted
    # if deleted = 1 then a note is deleted, and we can't see it running /friend or /friend/all
    # also we can't edit it
    deleted: Mapped[int] = mapped_column(Integer, default=0)

    def to_dict(self) -> dict:
        return {
            "user_id": self.user_id,
            "friend_id": self.friend_id,
            "note_id": self.id,
            "description": self.description,
            "score": self.score,
        }

    def remove(self) -> None:
        self.deleted = 1

    def restore(self) -> None:
        self.deleted = 0

    @staticmethod
    def is_valid_score(score: int) -> bool:
        return isinstance(score, int) and 1 <= score <= 5

    @staticmethod
    def is_valid_id(note_id: int) -> bool:
        note = (
            db.session.execute(db.select(Note).where(Note.id == note_id))
            .scalars()
            .all()
        )
        return bool(note)


with app.app_context():
    db.create_all()
