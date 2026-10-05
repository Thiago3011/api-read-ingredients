
from fastapi.testclient import TestClient

from app.main import app
from app.models.allergy import Allergy
from app.repositories.allergy_repository import AllergyRepository
from app.services.allergy_service import AllergyService


class FakeAllergy:
    def __init__(self, name):
        self.name = name


class FakeRepository:
    def get_all(self):
        return [
            FakeAllergy("Sulfato de níquel"),
            FakeAllergy("Nickel sulfate"),
            FakeAllergy("Cloreto de cobalto"),
        ]


# Testes do serviço

def test_should_identify_allergy_from_user_component():
    repository = FakeRepository()
    service = AllergyService(repository)

    result = service.check_allergies(
        user_components=["Sulfato de níquel"]
    )

    assert result == ["Sulfato de níquel"]


def test_should_ignore_non_allergy_component():
    repository = FakeRepository()
    service = AllergyService(repository)

    result = service.check_allergies(
        user_components=["Glicerina"]
    )

    assert result == []


def test_should_identify_allergy_from_ocr_text():
    repository = FakeRepository()
    service = AllergyService(repository)

    result = service.check_allergies(
        user_components=[],
        image_text="Ingredientes: água, Nickel sulfate, glicerina."
    )

    assert result == ["Nickel sulfate"]


def test_should_not_duplicate_allergy():
    repository = FakeRepository()
    service = AllergyService(repository)

    result = service.check_allergies(
        user_components=["Nickel sulfate"],
        image_text="Ingredientes: Nickel sulfate, glicerina."
    )

    assert result == ["Nickel sulfate"]


# Testes da API

def test_should_identify_allergy_through_api(client, monkeypatch):
    monkeypatch.setattr(
        AllergyRepository,
        "get_all",
        lambda self: [
            Allergy(name="Sulfato de níquel"),
            Allergy(name="Nickel sulfate"),
            Allergy(name="Cloreto de cobalto"),
        ],
    )

    response = client.post(
        "/validation/",
        data={"components": "Sulfato de níquel"},
    )

    assert response.status_code == 200
    assert response.json() == {
        "allergies": ["Sulfato de níquel"]
    }


def test_should_ignore_non_allergy_through_api(client, monkeypatch):
    monkeypatch.setattr(
        AllergyRepository,
        "get_all",
        lambda self: [
            Allergy(name="Sulfato de níquel"),
            Allergy(name="Nickel sulfate"),
            Allergy(name="Cloreto de cobalto"),
        ],
    )

    response = client.post(
        "/validation/",
        data={"components": "Glicerina"},
    )

    assert response.status_code == 200
    assert response.json() == {"allergies": []}


def test_should_identify_allergy_from_image_through_api(
    client, monkeypatch
):
    monkeypatch.setattr(
        AllergyRepository,
        "get_all",
        lambda self: [
            Allergy(name="Sulfato de níquel"),
            Allergy(name="Nickel sulfate"),
            Allergy(name="Cloreto de cobalto"),
        ],
    )

    class FakeImageProcessor:
        def __init__(self, image_file):
            self.image_file = image_file

        def process_image(self):
            return "Ingredientes: água, Nickel sulfate, glicerina."

    monkeypatch.setattr(
        "app.routers.validation.ImageProcessor",
        FakeImageProcessor,
    )

    response = client.post(
        "/validation/",
        files={
            "image": ("ingredientes.jpg", b"fake image", "image/jpeg")
        },
    )

    assert response.status_code == 200
    assert response.json() == {
        "allergies": ["Nickel sulfate"]
    }


def test_should_return_error_when_image_processing_fails(
    client, monkeypatch
):
    class FakeImageProcessor:
        def __init__(self, image_file):
            self.image_file = image_file

        def process_image(self):
            return "[ERRO] Falha ao processar imagem"

    monkeypatch.setattr(
        "app.routers.validation.ImageProcessor",
        FakeImageProcessor,
    )

    response = client.post(
        "/validation/",
        files={
            "image": ("ingredientes.jpg", b"fake image", "image/jpeg")
        },
    )

    assert response.status_code == 422
    assert response.json() == {
        "detail": "Não foi possível processar a imagem ou extrair texto."
    }