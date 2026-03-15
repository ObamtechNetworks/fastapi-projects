from fastapi.testclient import TestClient
import pytest
from app import models
from app.database import get_db, Base
from app.oauth2 import create_access_token
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


@pytest.fixture
def test_user(client):
    user_data = {"email": "alice@example.com", "password": "secret"}
    response = client.post("/users/", json=user_data)
    assert response.status_code == 201
    new_user = response.json()
    new_user["password"] = user_data["password"]
    return new_user

@pytest.fixture
def test_user2(client):
    user_data = {"email": "alice234@example.com", "password": "secret"}
    response = client.post("/users/", json=user_data)
    assert response.status_code == 201
    new_user = response.json()
    new_user["password"] = user_data["password"]
    return new_user

@pytest.fixture
def token(test_user, client):
    return create_access_token({"user_id": test_user["id"]})

@pytest.fixture
def authorized_client(client, token):
    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {token}"
    }
    return client

@pytest.fixture
def test_posts(test_user, session, test_user2):
    posts_data = [
        {"title": "First Post", "content": "Content of the first post", "owner_id": test_user["id"]},
        {"title": "Second Post", "content": "Content of the second post", "owner_id": test_user["id"]},
        {"title": "Third Post", "content": "Content of the third post", "owner_id": test_user["id"]},
        {"title": "Fourth Post", "content": "Content of the Fourth post", "owner_id": test_user2["id"]},

    ]
    def create_post_model(post):
        return models.Post(**post)
    
    post_map = map(create_post_model, posts_data)
    posts = list(post_map)

    session.add_all(posts)
    session.commit()

    return session.query(models.Post).all()