from sqlalchemy.orm import Session

from app.models.allergy import Allergy


class AllergyRepository:

    def __init__(self, db: Session):
        self.db = db

    def get_all(self) -> list[Allergy]:
        return self.db.query(Allergy).all()