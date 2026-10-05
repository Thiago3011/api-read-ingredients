from app.core.security import create_access_token, decode_access_token
from app.core.dependencies import get_current_user

def test_login_success(client, test_user):
    response = client.post(
        "/auth/login",
        json={
            "email": test_user["email"],
            "password": "123456"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_login_wrong_password(client, test_user):
    response = client.post(
        "/auth/login",
        json={
            "email": test_user["email"],
            "password": "senha_errada"
        }
    )

    assert response.status_code == 401

    data = response.json()

    assert data["detail"] == "Invalid email or password"


def test_login_nonexistent_user(client):
    response = client.post(
        "/auth/login",
        json={
            "email": "usuario_inexistente@email.com",
            "password": "123456"
        }
    )

    assert response.status_code == 401

    data = response.json()

    assert data["detail"] == "Invalid email or password"


def test_should_create_and_decode_access_token():
    data = {
        "sub": "1"
    }

    token = create_access_token(data)
    decoded = decode_access_token(token)

    assert decoded["sub"] == "1"
    assert "exp" in decoded
    
def test_should_get_current_user(client, test_user):
    login_response = client.post(
        "/auth/login",
        json={
            "email": test_user["email"],
            "password": "123456"
        }
    )

    token = login_response.json()["access_token"]

    response = client.get(
        "/user/",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 200
   
def test_validation_without_token(client):
    response = client.post(
        "/validation/",
        data={
            "components": ["leite"]
        }
    )

    assert response.status_code == 401


def test_validation_with_invalid_token(client):
    response = client.post(
        "/validation/",
        data={
            "components": ["leite"]
        },
        headers={
            "Authorization": "Bearer token_invalido"
        }
    )

    assert response.status_code == 401


def test_validation_with_valid_token(client, test_user):
    login_response = client.post(
        "/auth/login",
        json={
            "email": test_user["email"],
            "password": "123456"
        }
    )

    token = login_response.json()["access_token"]

    response = client.post(
        "/validation/",
        data={
            "components": ["leite"]
        },
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 200