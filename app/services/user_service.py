from app.repositories.user_repository import UserRepository 
from app.models.user import User
from app.schemas.user import UserCreate
from app.core.security import hash_password
from fastapi import HTTPException 


class UserService:

    def __init__(self, repository: UserRepository):
        self.repository = repository
        
    def find_user(self, email: str) -> User:
        user = self.repository.get_user(email)
        
        return user

    def get_users(self) -> list[User]:

        users = self.repository.get_all()

        return users
    
    def create_user(self, new_user_data: UserCreate) -> User:
        
        if self.find_user(new_user_data.email):
            raise HTTPException(status_code=409, detail="Email already registered")
        
        new_user = User(
            name=new_user_data.name,
            email=new_user_data.email,
            password_hash=hash_password(new_user_data.password)
        )
        
        return self.repository.create_user(new_user)