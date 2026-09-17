from fastapi import FastAPI
from app.routers.validation import router as validation_router

app = FastAPI(
    title="AllergyValidator",
    description="API para análise de ingredientes relacionados a alergias cadastradas.",
    version="2.0.0"
)

app.include_router(validation_router)

@app.get("/")
def root():
    return {"message": "AllergyValidator API funcionando!"}