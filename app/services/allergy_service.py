from app.repositories.allergy_repository import AllergyRepository


MAX_ALLERGY_NAME_LENGTH = 255


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

        if len(name) > MAX_ALLERGY_NAME_LENGTH:
            raise ValueError(
                f"O nome da alergia deve ter no máximo {MAX_ALLERGY_NAME_LENGTH} caracteres."
            )

        return self.repository.create(
            name=name,
            user_id=user_id
        )

    def create_allergies(
        self,
        names: list[str],
        user_id: int
    ) -> dict:
        """Create a batch of distinct allergies, skipping duplicates."""
        cleaned_names = []

        for raw_name in names:
            name = raw_name.strip().lstrip("•*-–— ").strip()

            if not name:
                continue

            if len(name) > MAX_ALLERGY_NAME_LENGTH:
                raise ValueError(
                    f"Cada alergia deve ter no máximo {MAX_ALLERGY_NAME_LENGTH} caracteres. "
                    "Separe cada item por linha, vírgula ou ponto e vírgula."
                )

            cleaned_names.append(name)

        if not cleaned_names:
            raise ValueError("Informe pelo menos uma alergia válida.")

        existing_names = {
            allergy.name.casefold()
            for allergy in self.repository.get_all(user_id)
        }
        seen_names = set()
        names_to_create = []
        skipped_count = 0

        for name in cleaned_names:
            normalized_name = name.casefold()

            if normalized_name in existing_names or normalized_name in seen_names:
                skipped_count += 1
                continue

            seen_names.add(normalized_name)
            names_to_create.append(name)

        if names_to_create:
            self.repository.create_many(
                names=names_to_create,
                user_id=user_id
            )

        return {
            "created_count": len(names_to_create),
            "skipped_count": skipped_count,
            "created_names": names_to_create
        }

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
        normalized_allergy_names = {
            name.casefold() for name in allergy_names
        }

        result = []
        matched_allergies = set()

        # Verifica os componentes informados pelo usuário.
        for component in user_components:
            normalized_component = component.casefold()

            if (
                normalized_component in normalized_allergy_names
                and normalized_component not in matched_allergies
            ):
                result.append(component)
                matched_allergies.add(normalized_component)

        # Verifica o texto extraído pelo OCR, sem repetir correspondências.
        if image_text:
            normalized_image_text = image_text.casefold()

            for allergy in allergy_names:
                normalized_allergy = allergy.casefold()

                if (
                    normalized_allergy in normalized_image_text
                    and normalized_allergy not in matched_allergies
                ):
                    result.append(allergy)
                    matched_allergies.add(normalized_allergy)

        return result
