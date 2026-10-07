def get_auth_headers(client, email, password="123456"):
    response = client.post(
        "/auth/login",
        json={
            "email": email,
            "password": password
        }
    )

    assert response.status_code == 200

    token = response.json()["access_token"]

    return {
        "Authorization": f"Bearer {token}"
    }


def test_should_create_allergy(
    client,
    test_user
):
    response = client.post(
        "/user/allergies/",
        params={
            "name": "Sulfato de níquel"
        },
        headers=get_auth_headers(
            client,
            test_user["email"]
        )
    )

    assert response.status_code == 200
    assert response.json()["name"] == "Sulfato de níquel"
    assert response.json()["user_id"] == test_user["id"]


def test_should_list_only_user_allergies(
    client,
    test_user
):
    headers = get_auth_headers(
        client,
        test_user["email"]
    )

    client.post(
        "/user/allergies/",
        params={
            "name": "Sulfato de níquel"
        },
        headers=headers
    )

    client.post(
        "/user/allergies/",
        params={
            "name": "Cloreto de cobalto"
        },
        headers=headers
    )

    response = client.get(
        "/user/allergies/",
        headers=headers
    )

    assert response.status_code == 200

    allergies = response.json()

    assert len(allergies) == 2
    assert allergies[0]["name"] == "Sulfato de níquel"
    assert allergies[1]["name"] == "Cloreto de cobalto"


def test_should_delete_own_allergy(
    client,
    test_user
):
    headers = get_auth_headers(
        client,
        test_user["email"]
    )

    create_response = client.post(
        "/user/allergies/",
        params={
            "name": "Sulfato de níquel"
        },
        headers=headers
    )

    allergy_id = create_response.json()["id"]

    response = client.delete(
        f"/user/allergies/{allergy_id}",
        headers=headers
    )

    assert response.status_code == 200
    assert response.json() == {
        "message": "Alergia removida com sucesso!"
    }

    list_response = client.get(
        "/user/allergies/",
        headers=headers
    )

    assert list_response.status_code == 200
    assert list_response.json() == []


def test_should_not_allow_user_to_delete_another_user_allergy(
    client,
    test_user
):
    first_user_headers = get_auth_headers(
        client,
        test_user["email"]
    )

    create_response = client.post(
        "/user/allergies/",
        params={
            "name": "Sulfato de níquel"
        },
        headers=first_user_headers
    )

    allergy_id = create_response.json()["id"]

    second_user_response = client.post(
        "/user/",
        json={
            "name": "Second User",
            "email": "second@example.com",
            "password": "123456"
        }
    )

    assert second_user_response.status_code == 200

    second_user_headers = get_auth_headers(
        client,
        "second@example.com"
    )

    response = client.delete(
        f"/user/allergies/{allergy_id}",
        headers=second_user_headers
    )

    assert response.status_code == 404
    assert response.json() == {
        "detail": "Alergia não encontrada."
    }


def test_should_not_show_another_user_allergy(
    client,
    test_user
):
    first_user_headers = get_auth_headers(
        client,
        test_user["email"]
    )

    client.post(
        "/user/allergies/",
        params={
            "name": "Sulfato de níquel"
        },
        headers=first_user_headers
    )

    second_user_response = client.post(
        "/user/",
        json={
            "name": "Second User",
            "email": "second@example.com",
            "password": "123456"
        }
    )

    assert second_user_response.status_code == 200

    second_user_headers = get_auth_headers(
        client,
        "second@example.com"
    )

    response = client.get(
        "/user/allergies/",
        headers=second_user_headers
    )

    assert response.status_code == 200
    assert response.json() == []