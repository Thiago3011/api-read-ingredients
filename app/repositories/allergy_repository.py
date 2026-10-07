from sqlalchemy.orm import Session

from app.models.allergy import Allergy


class AllergyRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self, user_id: int) -> list[Allergy]:
        return (
            self.db.query(Allergy)
            .filter(Allergy.user_id == user_id)
            .all()
        )

    def get_by_id(
        self,
        allergy_id: int,
        user_id: int
    ) -> Allergy | None:
        return (
            self.db.query(Allergy)
            .filter(
                Allergy.id == allergy_id,
                Allergy.user_id == user_id
            )
            .first()
        )

    def create(
        self,
        name: str,
        user_id: int
    ) -> Allergy:
        allergy = Allergy(
            name=name,
            user_id=user_id
        )

        self.db.add(allergy)
        self.db.commit()
        self.db.refresh(allergy)

        return allergy

    def delete(
        self,
        allergy: Allergy
    ) -> None:
        self.db.delete(allergy)
        self.db.commit()