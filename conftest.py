import pytest
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, text
from model import Base
from repository import TaskRepository

TEST_DATABASE_URL = "postgresql+psycopg2://postgres:password123@localhost:5431/test_postgres"
test_engine = create_engine(TEST_DATABASE_URL)
TestingSession = sessionmaker(bind=test_engine)

@pytest.fixture(scope='session', autouse=True)
def setup_db():
    Base.metadata.create_all(bind=test_engine)
    yield
    Base.metadata.drop_all(bind=test_engine)


@pytest.fixture(scope='function')
def db_session():
    session = TestingSession()
    yield session

    session.close()
    with (test_engine.connect() as con):
        con.execute(text("TRUNCATE TABLE tasks RESTART IDENTITY CASCADE;"))
        con.commit()


@pytest.fixture
def repository(db_session):
    return TaskRepository(db_session)
