from fastapi import Depends, FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.database import get_db

from app.routers.validation import router as validation_router
from app.routers.user import router as user_router
from app.routers.auth import router as auth_router
from app.routers.user_allergy import router as user_allergy


app = FastAPI(
    title="AllergyValidator",
    description="API para análise de ingredientes relacionados a alergias cadastradas.",
    version="2.0.0"
)

app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(validation_router)
app.include_router(user_router)
app.include_router(auth_router)
app.include_router(user_allergy)


@app.get("/health", tags=["health"])
def health_check(db: Session = Depends(get_db)):
    """Report application readiness only when the database can be reached."""
    try:
        db.execute(text("SELECT 1"))
    except SQLAlchemyError as exc:
        raise HTTPException(
            status_code=503,
            detail="Database unavailable"
        ) from exc

    return {"status": "ok", "database": "ok"}


@app.get("/")
def root():
    return FileResponse("templates/index.html")