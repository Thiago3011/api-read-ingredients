from app.repositories.user_repository import UserRepository 
from app.models.user import User


class UserService:

    def __init__(self, repository: UserRepository):
        self.repository = repository

    def get_users(self) -> list[User]:

        users = self.repository.get_all()

        return users