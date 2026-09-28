from sqlalchemy.orm import Session

from app.models.user import User

class UserRepository:

    def __init__(self, db: Session):
        self.db = db

    def get_all(self) -> list[User]:
        return self.db.query(User).all()
    
    def get_user_by_id(self, user_id: int) -> User | None:
        return self.db.query(User).filter(User.id == user_id).first()
    
    def get_user_by_email(self, user_email: str) -> User | None:
        return self.db.query(User).filter(User.email == user_email).first()

    def create_user(self, new_user_data: User) -> User:
        self.db.add(new_user_data)
        self.db.commit()
        self.db.refresh(new_user_data)
        
        return new_user_data
    
    def update_user(self, updated_user_data: User) -> User:
        self.db.commit()
        self.db.refresh(updated_user_data)
        
        return updated_user_data
    
    def delete_user(self, user: User) -> dict:
        self.db.delete(user)
        self.db.commit()
        
        return {"message": "User deleted!"}