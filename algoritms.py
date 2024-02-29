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
)  # import engine to create connections with db
from sqlalchemy.dialects import postgresql

url = "postgresql+psycopg://postgres:Konorra9@127.0.0.1:5432/postgres"
engine = create_engine(url, echo=True)  # ready to connect
metadata = MetaData()  # one metadata = one dataase
fake = Faker()

clients_table = Table(
    "clients",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("first_name", String, nullable=True),
    Column("last_name", String, nullable=True),
)
orders_table = Table(
    "orders",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("client_id", Integer, ForeignKey("clients.id")),
    Column("description", String),
)

metadata.create_all(engine)  # create tables

# create insert query
stmt = insert(orders_table).values(client_id=1, description=fake.text())
postgres_stmt = stmt.compile(engine, postgresql.dialect())

stmt_wo_values = insert(orders_table)  # without values, possible to insert a few rows

with engine.begin() as connection:  # type: Connection
    # do insert 'without' values
    connection.execute(
        stmt_wo_values,
        [
            {"client_id": 2, "description": fake.text()},
            {"client_id": 2, "description": fake.text()},
            {"client_id": 2, "description": fake.text()},
        ],
    )
    # do insert with values
    connection.execute(postgres_stmt)
