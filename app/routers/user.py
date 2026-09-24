from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.repositories.user_repository import UserRepository
from app.schemas.user import UserCreate
from app.services.user_service import UserService

router = APIRouter(
    prefix="/user",
    tags=["user"]
)


@router.get("/")
def get_users(db: Session = Depends(get_db)):
    
    service = UserService(UserRepository(db))
    
    return service.get_users()

@router.post("/")
def create_user(new_user: UserCreate, db: Session = Depends(get_db)):
    service = UserService(UserRepository(db))
    
    return service.create_user(new_user)