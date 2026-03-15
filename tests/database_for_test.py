from fastapi.testclient import TestClient
import pytest
from app.database import get_db, Base
from app.main import app
from sqlalchemy.orm import  sessionmaker
from sqlalchemy import create_engine

# format => postgresql://<username>:<password>@<ip-address/hostname>/<database_name>
TEST_DATABASE_URL = 'postgresql://postgres:root@localhost:5432/fastapi_test'
# SQL_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}" 

# create an engine instance
engine = create_engine(TEST_DATABASE_URL)

# create a SessionLocal class
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# create all tables in the test database
# Base.metadata.create_all(bind=engine)

# Create dependency to get a database session for each request
# def override_get_db():
#     db = TestingSessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()

# app.dependency_overrides[get_db] = override_get_db

# client = TestClient(app)


@pytest.fixture()
def session():
    # run setup code before the test
    Base.metadata.drop_all(bind=engine)  # drop all tables before each test
    Base.metadata.create_all(bind=engine) # create all tables before each test
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture()
def client(session):
    def override_get_db():
        try:
            yield session
        finally:
            session.close()
    app.dependency_overrides[get_db] = override_get_db

    yield TestClient(app)