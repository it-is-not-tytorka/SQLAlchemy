from faker import Faker
from sqlalchemy import (
    ForeignKey,
    String,
    Integer,
    Table,
    Column,
    MetaData,
    create_engine,
    insert,
    Connection,
    select,
    or_,
    desc,
    and_, text, update, bindparam, delete, inspect,
)  # import engine to create connections with db
from sqlalchemy.dialects import postgresql
from sqlalchemy.orm import mapped_column, Mapped, as_declarative, Session, relationship

url = "postgresql+psycopg://postgres:Konorra9@127.0.0.1:5432/northwind"
engine = create_engine(url, echo=True)  # ready to connect
metadata = MetaData()  # one metadata = one database
session = Session(engine, expire_on_commit=True, autoflush=False)
fake = Faker()

user_table = Table(
    'users',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('user_name', String)
)

phone_number = Table(
    'phones',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('phone_number', String),
    Column('user_fk', Integer, ForeignKey('users.id'))
)

metadata.create_all(engine)

@as_declarative()
class AbstractModel:
    id: Mapped[int] = mapped_column(autoincrement=True, primary_key=True)

class UserModel(AbstractModel):
    __tablename__ = "users"
    user_name: Mapped[str] = mapped_column()
    phone: Mapped["PhoneModel"] = relationship(back_populates="user", uselist=False)

    def __repr__(self):
        return f'User: {self.user_name}'


class PhoneModel(AbstractModel):
    __tablename__ = 'phones'
    phone_number: Mapped[str] = mapped_column()
    user: Mapped["UserModel"] = relationship(back_populates="phone", uselist=False)   # uselist=True - Many to one, uselist=False - One to one
    user_fk: Mapped[int] = mapped_column(ForeignKey('users.id'))

    def __repr__(self):
        return f"Phone: {self.phone_number=}, {self.user_fk=}"

user = UserModel(user_name='First')
phone = PhoneModel(phone_number='89009009090')
user.phone = phone
session.add(user)
session.commit()

users = session.scalars(select(UserModel)).all()
phones = session.scalars(select(PhoneModel)).all()

print(users)
print(phones)