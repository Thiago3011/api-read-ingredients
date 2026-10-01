from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.repositories.user_repository import UserRepository
from app.schemas.user import UserCreate, UserUpdate, UserResponse
from app.services.user_service import UserService

router = APIRouter(
    prefix="/user",
    tags=["user"]
)

@router.get("/", response_model=list[UserResponse])
def get_users(db: Session = Depends(get_db)):
    
    service = UserService(UserRepository(db))
    
    return service.get_users()

@router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    service = UserService(UserRepository(db))
    
    return service.get_user(user_id)

@router.post("/", response_model=UserResponse)
def create_user(new_user: UserCreate, db: Session = Depends(get_db)):
    service = UserService(UserRepository(db))
    
    return service.create_user(new_user)

@router.patch("/{user_id}", response_model=UserResponse)
def update_user(user_id: int, updated_user: UserUpdate, db: Session = Depends(get_db)):
    service = UserService(UserRepository(db))
    
    return service.update_user(user_id, updated_user)

@router.delete("/{user_id}", status_code=204)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    service = UserService(UserRepository(db))
    
    return service.delete_user(user_id)