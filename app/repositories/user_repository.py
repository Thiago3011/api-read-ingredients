from sqlalchemy.orm import Session

from app.models.user import User

class UserRepository:

    def __init__(self, db: Session):
        self.db = db

    def get_all(self) -> list[User]:
        return self.db.query(User).all()
    
    def get_user(self, email: str) -> User | None:
        return self.db.query(User).filter(User.email == email).first()
    
    def create_user(self, new_user_data: User) -> User:
        self.db.add(new_user_data)
        self.db.commit()
        self.db.refresh(new_user_data)
        
        return new_user_data