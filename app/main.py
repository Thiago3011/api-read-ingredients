from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from app.routers.validation import router as validation_router


app = FastAPI(
    title="AllergyValidator",
    description="API para análise de ingredientes relacionados a alergias cadastradas.",
    version="2.0.0"
)

app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(validation_router)


@app.get("/")
def root():
    return FileResponse("templates/index.html")