from fastapi import HTTPException

from app.core.security import create_access_token, verify_password
from app.repositories.user_repository import UserRepository
from app.schemas.user import LoginRequest


class AuthService:

    def __init__(self, repository: UserRepository):
        self.repository = repository

    def login(self, login_data: LoginRequest) -> dict:
        user = self.repository.get_user_by_email(login_data.email)

        if user is None:
            raise HTTPException(
                status_code=401,
                detail="Invalid email or password"
            )

        if not verify_password(
            login_data.password,
            user.password_hash
        ):
            raise HTTPException(
                status_code=401,
                detail="Invalid email or password"
            )

        access_token = create_access_token(
            {"sub": str(user.id)}
        )

        return {
            "access_token": access_token,
            "token_type": "bearer"
        }