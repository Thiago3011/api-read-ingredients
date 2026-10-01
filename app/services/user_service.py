from app.repositories.user_repository import UserRepository 
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate
from app.core.security import hash_password
from fastapi import HTTPException 


class UserService:

    def __init__(self, repository: UserRepository):
        self.repository = repository
        
    def find_user(self, user_id: int | None = None, user_email: str | None = None) -> User | None:
        if user_id is not None:
            return self.repository.get_user_by_id(user_id)
        if user_email is not None:
            return self.repository.get_user_by_email(user_email)
        
        return None

    def get_users(self) -> list[User]:
        
        return self.repository.get_all()

    def get_user(self, user_id: int) -> User:
        
        user = self.repository.get_user_by_id(user_id)
        
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")
        
        return user
    
    def create_user(self, new_user_data: UserCreate) -> User:
        
        if self.find_user(user_email=new_user_data.email):
            raise HTTPException(status_code=409, detail="Email already registered")
        
        new_user = User(
            name=new_user_data.name,
            email=new_user_data.email,
            password_hash=hash_password(new_user_data.password)
        )
        
        return self.repository.create_user(new_user)
    
    def update_user(self, user_id: int, updated_user_data: UserUpdate) -> User:
        user = self.find_user(user_id)
        
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")

        if updated_user_data.email is not None:
            existing_user = self.find_user(
                user_email=updated_user_data.email
            )

            if existing_user and existing_user.id != user.id:
                raise HTTPException(
                    status_code=409,
                    detail="Email already registered"
                )

        if updated_user_data.name is not None:
            user.name = updated_user_data.name

        if updated_user_data.email is not None:
            user.email = updated_user_data.email

        if updated_user_data.password is not None:
            user.password_hash = hash_password(updated_user_data.password)

        return self.repository.update_user(user)
    
    def delete_user(self, user_id: int) -> dict:
        
        user = self.find_user(user_id=user_id)
        
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")
        
        return self.repository.delete_user(user)
        