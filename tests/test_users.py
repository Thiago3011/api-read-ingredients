import pytest

from fastapi import HTTPException

from app.services.user_service import UserService
from app.schemas.user import UserCreate, UserUpdate
from app.models.user import User

from app.core.security import create_access_token, decode_access_token


# ==========================================
# Fake Repository
# ==========================================


class FakeUserRepository:

    def __init__(self):
        self.users = []
        self.next_id = 1

    def get_all(self):
        return self.users

    def get_user_by_id(self, user_id: int):
        return next(
            (user for user in self.users if user.id == user_id),
            None
        )

    def get_user_by_email(self, user_email: str):
        return next(
            (user for user in self.users if user.email == user_email),
            None
        )

    def create_user(self, new_user_data: User):
        new_user_data.id = self.next_id
        self.next_id += 1
        self.users.append(new_user_data)
        return new_user_data

    def update_user(self, updated_user_data: User):
        return updated_user_data

    def delete_user(self, user: User):
        self.users.remove(user)
        return {"message": "User deleted!"}


# ==========================================
# CREATE
# ==========================================


def test_should_create_user_successfully():
    repository = FakeUserRepository()
    service = UserService(repository)

    new_user = UserCreate(
        name="Thiago",
        email="thiago@example.com",
        password="SenhaSegura123"
    )

    result = service.create_user(new_user)

    assert result.id == 1
    assert result.name == "Thiago"
    assert result.email == "thiago@example.com"
    assert result.password_hash != "SenhaSegura123"
    assert len(repository.users) == 1


def test_should_not_create_user_with_duplicate_email():
    repository = FakeUserRepository()
    service = UserService(repository)

    user1 = UserCreate(
        name="Thiago",
        email="thiago@example.com",
        password="SenhaSegura123"
    )

    user2 = UserCreate(
        name="Maria",
        email="thiago@example.com",
        password="OutraSenha456"
    )

    service.create_user(user1)

    with pytest.raises(HTTPException) as exc:
        service.create_user(user2)

    assert exc.value.status_code == 409
    assert exc.value.detail == "Email already registered"
    assert len(repository.users) == 1


# ==========================================
# READ
# ==========================================


def test_should_get_user_by_id():
    repository = FakeUserRepository()
    service = UserService(repository)

    new_user = UserCreate(
        name="Thiago",
        email="thiago@example.com",
        password="SenhaSegura123"
    )

    created_user = service.create_user(new_user)

    result = service.get_user(created_user.id)

    assert result.id == created_user.id
    assert result.name == "Thiago"
    assert result.email == "thiago@example.com"


def test_should_raise_error_when_user_not_found():
    repository = FakeUserRepository()
    service = UserService(repository)

    with pytest.raises(HTTPException) as exc:
        service.get_user(999)

    assert exc.value.status_code == 404
    assert exc.value.detail == "User not found"


def test_should_get_all_users():
    repository = FakeUserRepository()
    service = UserService(repository)

    user1 = UserCreate(
        name="Thiago",
        email="thiago1@example.com",
        password="SenhaSegura123"
    )

    user2 = UserCreate(
        name="Maria",
        email="maria@example.com",
        password="SenhaSegura456"
    )

    service.create_user(user1)
    service.create_user(user2)

    result = service.get_users()

    assert len(result) == 2
    assert result[0].name == "Thiago"
    assert result[1].name == "Maria"


# ==========================================
# UPDATE
# ==========================================


def test_should_update_user():
    repository = FakeUserRepository()
    service = UserService(repository)

    new_user = UserCreate(
        name="Thiago",
        email="thiago@example.com",
        password="SenhaSegura123"
    )

    created_user = service.create_user(new_user)

    updated_data = UserUpdate(name="Thiago Henrique")

    result = service.update_user(created_user.id, updated_data)

    assert result.id == created_user.id
    assert result.name == "Thiago Henrique"
    assert result.email == "thiago@example.com"


def test_should_update_user_password():
    repository = FakeUserRepository()
    service = UserService(repository)

    new_user = UserCreate(
        name="Thiago",
        email="thiago@example.com",
        password="SenhaSegura123"
    )

    created_user = service.create_user(new_user)
    old_password_hash = created_user.password_hash

    updated_data = UserUpdate(password="NovaSenha456")

    result = service.update_user(created_user.id, updated_data)

    assert result.password_hash != old_password_hash
    assert result.password_hash != "NovaSenha456"


def test_should_not_update_user_with_duplicate_email():
    repository = FakeUserRepository()
    service = UserService(repository)

    user1 = service.create_user(
        UserCreate(
            name="Thiago",
            email="thiago@example.com",
            password="SenhaSegura123"
        )
    )

    user2 = service.create_user(
        UserCreate(
            name="Maria",
            email="maria@example.com",
            password="OutraSenha456"
        )
    )

    updated_data = UserUpdate(email="maria@example.com")

    with pytest.raises(HTTPException) as exc:
        service.update_user(user1.id, updated_data)

    assert exc.value.status_code == 409
    assert exc.value.detail == "Email already registered"
    assert user1.email == "thiago@example.com"
    assert user2.email == "maria@example.com"


def test_should_raise_error_when_updating_nonexistent_user():
    repository = FakeUserRepository()
    service = UserService(repository)

    updated_data = UserUpdate(name="Novo Nome")

    with pytest.raises(HTTPException) as exc:
        service.update_user(999, updated_data)

    assert exc.value.status_code == 404
    assert exc.value.detail == "User not found"
    assert len(repository.users) == 0


def test_should_update_user_keeping_same_email():
    repository = FakeUserRepository()
    service = UserService(repository)

    user = service.create_user(
        UserCreate(
            name="Thiago",
            email="thiago@example.com",
            password="SenhaSegura123"
        )
    )

    updated_data = UserUpdate(
        name="Thiago Henrique",
        email="thiago@example.com"
    )

    result = service.update_user(user.id, updated_data)

    assert result.name == "Thiago Henrique"
    assert result.email == "thiago@example.com"
    assert len(repository.users) == 1


def test_should_update_user_with_new_email():
    repository = FakeUserRepository()
    service = UserService(repository)

    user = service.create_user(
        UserCreate(
            name="Thiago",
            email="thiago@example.com",
            password="SenhaSegura123"
        )
    )

    updated_data = UserUpdate(email="thiago.novo@example.com")

    result = service.update_user(user.id, updated_data)

    assert result.email == "thiago.novo@example.com"
    assert repository.get_user_by_email("thiago@example.com") is None
    assert repository.get_user_by_email("thiago.novo@example.com") == user


# ==========================================
# DELETE
# ==========================================


def test_should_delete_user():
    repository = FakeUserRepository()
    service = UserService(repository)

    new_user = UserCreate(
        name="Thiago",
        email="thiago@example.com",
        password="SenhaSegura123"
    )

    created_user = service.create_user(new_user)

    result = service.delete_user(created_user.id)

    assert result == {"message": "User deleted!"}
    assert len(repository.users) == 0


def test_should_raise_error_when_deleting_nonexistent_user():
    repository = FakeUserRepository()
    service = UserService(repository)

    with pytest.raises(HTTPException) as exc:
        service.delete_user(999)

    assert exc.value.status_code == 404
    assert exc.value.detail == "User not found"
    assert len(repository.users) == 0


# ==========================================
# API ROUTES
# ==========================================


def test_should_return_users_list(client, test_user):
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


def test_should_create_user_through_api(client):
    response = client.post(
        "/user/",
        json={
            "name": "Thiago",
            "email": "thiago@example.com",
            "password": "SenhaSegura123"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["name"] == "Thiago"
    assert data["email"] == "thiago@example.com"
    assert "password_hash" not in data
    assert "password" not in data


def test_should_get_user_through_api(client, test_user):
    user_id = test_user["id"]

    login_response = client.post(
        "/auth/login",
        json={
            "email": test_user["email"],
            "password": "123456"
        }
    )

    token = login_response.json()["access_token"]

    response = client.get(
        f"/user/{user_id}",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == user_id
    assert data["name"] == test_user["name"]
    assert data["email"] == test_user["email"]
    assert "password_hash" not in data


def test_should_update_user_through_api(client):
    create_response = client.post(
        "/user/",
        json={
            "name": "Thiago",
            "email": "thiago@example.com",
            "password": "SenhaSegura123"
        }
    )

    user_id = create_response.json()["id"]

    login_response = client.post(
        "/auth/login",
        json={
            "email": "thiago@example.com",
            "password": "SenhaSegura123"
        }
    )

    token = login_response.json()["access_token"]

    response = client.patch(
        f"/user/{user_id}",
        json={
            "name": "Thiago Henrique"
        },
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == user_id
    assert data["name"] == "Thiago Henrique"
    assert data["email"] == "thiago@example.com"
    assert "password_hash" not in data


def test_should_return_404_when_updating_nonexistent_user(
    client,
    test_user
):
    login_response = client.post(
        "/auth/login",
        json={
            "email": test_user["email"],
            "password": "123456"
        }
    )

    token = login_response.json()["access_token"]

    response = client.patch(
        "/user/999",
        json={
            "name": "Novo Nome"
        },
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 403
    assert response.json()["detail"] == "You can only update your own user"


def test_should_delete_user_through_api(client):
    create_response = client.post(
        "/user/",
        json={
            "name": "Thiago",
            "email": "thiago@example.com",
            "password": "SenhaSegura123"
        }
    )

    user_id = create_response.json()["id"]

    login_response = client.post(
        "/auth/login",
        json={
            "email": "thiago@example.com",
            "password": "SenhaSegura123"
        }
    )

    token = login_response.json()["access_token"]

    response = client.delete(
        f"/user/{user_id}",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 204


def test_should_return_404_when_deleting_nonexistent_user(
    client,
    test_user
):
    login_response = client.post(
        "/auth/login",
        json={
            "email": test_user["email"],
            "password": "123456"
        }
    )

    token = login_response.json()["access_token"]

    response = client.delete(
        "/user/999",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 403
    assert response.json()["detail"] == "You can only delete your own user"


def test_should_return_409_when_creating_duplicate_email(client):
    client.post(
        "/user/",
        json={
            "name": "Thiago",
            "email": "thiago@example.com",
            "password": "SenhaSegura123"
        }
    )

    response = client.post(
        "/user/",
        json={
            "name": "Maria",
            "email": "thiago@example.com",
            "password": "OutraSenha456"
        }
    )

    assert response.status_code == 409
    assert response.json()["detail"] == "Email already registered"


def test_should_return_409_when_updating_to_duplicate_email(client):
    user1_response = client.post(
        "/user/",
        json={
            "name": "Thiago",
            "email": "thiago@example.com",
            "password": "SenhaSegura123"
        }
    )

    user1_id = user1_response.json()["id"]

    client.post(
        "/user/",
        json={
            "name": "Maria",
            "email": "maria@example.com",
            "password": "OutraSenha456"
        }
    )

    login_response = client.post(
        "/auth/login",
        json={
            "email": "thiago@example.com",
            "password": "SenhaSegura123"
        }
    )

    token = login_response.json()["access_token"]

    response = client.patch(
        f"/user/{user1_id}",
        json={
            "email": "maria@example.com"
        },
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 409
    assert response.json()["detail"] == "Email already registered"


def test_should_return_422_when_creating_user_without_required_fields(client):
    response = client.post(
        "/user/",
        json={
            "name": "Thiago"
        }
    )

    assert response.status_code == 422


# ==========================================
# JWT
# ==========================================


def test_should_create_and_decode_access_token():
    data = {
        "sub": "test@example.com"
    }

    token = create_access_token(data)
    decoded = decode_access_token(token)

    assert decoded["sub"] == "test@example.com"
    assert "exp" in decoded


def test_get_users_without_token(client):
    response = client.get("/user/")

    assert response.status_code == 401


def test_get_users_with_valid_token(client, test_user):
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