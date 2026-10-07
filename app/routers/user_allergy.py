from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.core.dependencies import get_current_user
from app.repositories.allergy_repository import AllergyRepository
from app.services.allergy_service import AllergyService


router = APIRouter(
    prefix="/user/allergies",
    tags=["User Allergies"]
)


@router.get("/")
def get_user_allergies(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    service = AllergyService(AllergyRepository(db))

    return service.get_user_allergies(
        user_id=current_user.id
    )


@router.post("/")
def create_allergy(
    name: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    service = AllergyService(AllergyRepository(db))

    try:
        return service.create_allergy(
            name=name,
            user_id=current_user.id
        )
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail=str(e)
        ) from e


@router.delete("/{allergy_id}")
def delete_allergy(
    allergy_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    service = AllergyService(AllergyRepository(db))

    deleted = service.delete_allergy(
        allergy_id=allergy_id,
        user_id=current_user.id
    )

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="Alergia não encontrada."
        )

    return {
        "message": "Alergia removida com sucesso!"
    }