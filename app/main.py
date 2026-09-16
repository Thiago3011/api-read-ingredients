from fastapi import FastAPI

app = FastAPI(
    title="AllergyValidator",
    description="API para análise de ingredientes relacionados a alergias cadastradas.",
    version="2.0.0"
)

@app.get("/")
def root():
    return {"message": "AllergyValidator API funcionando!"}