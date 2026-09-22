from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.repositories.user_repository import UserRepository
from app.services.user_service import UserService

router = APIRouter(
    prefix="/user",
    tags=["user"]
)


@router.get("/")
def get_users(db: Session = Depends(get_db)):
    
    service = UserService(UserRepository(db))
    
    return service.get_users()