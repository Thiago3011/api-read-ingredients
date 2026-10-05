from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.repositories.user_repository import UserRepository
from app.schemas.user import LoginRequest
from app.services.auth_service import AuthService


router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)


@router.post("/login")
def login(
    login_data: LoginRequest,
    db: Session = Depends(get_db)
):
    service = AuthService(UserRepository(db))

    return service.login(login_data)