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