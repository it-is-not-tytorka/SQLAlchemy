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
    Connection, select, or_, desc
)  # import engine to create connections with db
from sqlalchemy.dialects import postgresql

url = "postgresql+psycopg://postgres:Konorra9@127.0.0.1:5432/postgres"
engine = create_engine(url, echo=True)  # ready to connect
metadata = MetaData()  # one metadata = one dataase
fake = Faker()

classes_table = Table(
    'classes',
    metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('teacher_name', String, nullable=True),
)

students_table = Table(
    'students',
    metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('first_name', String, nullable=True),
    Column('last_name', String, nullable=True),
    Column('class_id', Integer, ForeignKey('classes.id')),
)

metadata.create_all(engine)
stmt = insert(students_table).values(
    first_name=fake.first_name(),
    last_name=fake.last_name(),
    class_id=1,
)

postgres_stmt = stmt.compile(engine, postgresql.dialect())
with engine.begin() as connection:   # type: Connection  # this piece of shit gives type hints
    result = connection.execute(
        select(students_table).where(
            or_(students_table.c.first_name.startswith('L'),   # possible to use python methods
            students_table.c.last_name.contains('o'))
        )
    )
    print(result.all())

    result = connection.execute(
        select(
            classes_table,
            (students_table.c.first_name + ' ' + students_table.c.last_name).label('student_name'),
            students_table.c.id.label('student_id')
        ).where(
            students_table.c.id.in_([1,3])
        ).join_from(classes_table, students_table)  # the same with students_table.c.class_id == classes_table.c.id
        # the same join(classes_table)
        # there's left_join, right_join etc
        .order_by(
            desc(students_table.c.id)
        ).group_by(
            ...
        ).having(
            ...
        )
    )
    print(result.mappings().all())