from app.repositories.allergy_repository import AllergyRepository


class AllergyService:

    def __init__(self, repository: AllergyRepository):
        self.repository = repository

    def check_allergies(
        self,
        user_components: list[str],
        image_text: str = "",
    ) -> list[str]:

        allergies = self.repository.get_all()

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