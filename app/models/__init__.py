"""SQLAlchemy models registered in Base.metadata."""

from app.models.allergy import Allergy
from app.models.user import User

__all__ = ["Allergy", "User"]
