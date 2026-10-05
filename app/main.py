from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from app.routers.validation import router as validation_router
from app.routers.user import router as user_router
from app.routers.auth import router as auth_router


app = FastAPI(
    title="AllergyValidator",
    description="API para análise de ingredientes relacionados a alergias cadastradas.",
    version="2.0.0"
)

app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(validation_router)
app.include_router(user_router)
app.include_router(auth_router)

@app.get("/")
def root():
    return FileResponse("templates/index.html")