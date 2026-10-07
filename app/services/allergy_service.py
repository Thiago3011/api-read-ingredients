from app.repositories.allergy_repository import AllergyRepository


class AllergyService:
    def __init__(self, repository: AllergyRepository):
        self.repository = repository

    def get_user_allergies(self, user_id: int):
        return self.repository.get_all(user_id)

    def create_allergy(
        self,
        name: str,
        user_id: int
    ):
        name = name.strip()

        if not name:
            raise ValueError("O nome da alergia não pode estar vazio.")

        return self.repository.create(
            name=name,
            user_id=user_id
        )

    def delete_allergy(
        self,
        allergy_id: int,
        user_id: int
    ) -> bool:
        allergy = self.repository.get_by_id(
            allergy_id=allergy_id,
            user_id=user_id
        )

        if not allergy:
            return False

        self.repository.delete(allergy)

        return True

    def check_allergies(
        self,
        user_id: int,
        user_components: list[str],
        image_text: str = "",
    ) -> list[str]:

        allergies = self.repository.get_all(user_id)

        allergy_names = [allergy.name for allergy in allergies]

        result = []

        # Verifica os componentes informados pelo usuário
        for component in user_components:
            if component.lower() in [
                allergy.lower() for allergy in allergy_names
            ]:
                result.append(component)

        # Verifica o texto extraído pelo OCR
        if image_text:
            for allergy in allergy_names:
                if (
                    allergy.lower() in image_text.lower()
                    and allergy not in result
                ):
                    result.append(allergy)

        return result