import pytest
from jose import jwt
from app.config import settings
from app import schemas

# def test_root(client):
#     response = client.get("/")
#     print(response.json().get("message"))
#     assert response.status_code == 200
    
def test_create_user(client):
    response = client.post("/users/", json={"email": "alice@example.com", "password": "secret"})
    new_user = schemas.UserOut(**response.json())
    assert new_user.email == "alice@example.com"
    assert response.status_code == 201


def test_login_user(test_user, client):
    response = client.post("/auth/login/", data={"username": test_user["email"], "password": test_user["password"]})
    login_response = schemas.Token(**response.json())
    payload = jwt.decode(login_response.access_token, settings.secret_key, algorithms=[settings.algorithm])
    id = payload.get("user_id")
    
    assert response.status_code == 200
    assert id == test_user["id"]
    assert login_response.token_type == "bearer"

@pytest.mark.parametrize("email, password, status_code", [
    ("alice@example.com", "wrongpassword", 403),
    ("nonexistent@example.com", "password", 403),
    # no email no password 
    ("", "", 422),
    # wrong email wrong password
    ("wrong@example.com", "wrongpassword", 403),
    # wrong email formats
    ("invalid-email", "password", 403),
    # right email no password
    ("alice@example.com", "", 422),

])
def test_incorrect_login(test_user, client, email, password, status_code):
    response = client.post("/auth/login/", data={"username": email, "password": password})
    assert response.status_code == status_code
