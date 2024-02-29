import datetime
from sqlalchemy import (
    ForeignKey,
    Date,
    String,
    Integer,
    Table,
    Column,
    MetaData,
    create_engine,
    select,
)  # import engine to create connections with db
from sqlalchemy.orm import as_declarative, mapped_column, Mapped, Session, declared_attr

url = "postgresql+psycopg://postgres:Konorra9@127.0.0.1:5432/northwind"
engine = create_engine(url, echo=True)  # ready to connect
metadata = MetaData()  # one metadata = one dataase


user_table = Table(
    "users",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("user_name", String),
    Column("date_registration", Date),
    Column("team_id", Integer, ForeignKey("teams.id")),
)
team_table = Table(
    "teams",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("team_name", String),
)
metadata.create_all(engine)


@as_declarative()
class AbstractModel:
    id: Mapped[int] = mapped_column(autoincrement=True, primary_key=True)

    @classmethod
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()


class UserModel(AbstractModel):
    __tablename__ = "users"
    user_name: Mapped[str] = mapped_column()
    date_registration: Mapped[datetime.date] = mapped_column(Date)
    team_id: Mapped[int] = mapped_column(ForeignKey("teams.id"))


class TeamModel(AbstractModel):
    __tablename__ = "teams"
    team_name: Mapped[str] = mapped_column(String)


team = TeamModel(team_name="B")
user = UserModel(
    id=7, user_name="Trick", team_id=1, date_registration=datetime.date.today()
)

with Session(engine) as session:
    with session.begin():
        AbstractModel.metadata.create_all(engine)
    with session.begin():
        res = session.execute(select(UserModel).where(UserModel.team_id == 1))
        cursor = res.scalars()
        for user in cursor.all():
            print(user.id)
