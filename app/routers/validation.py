from fastapi import APIRouter, Depends, File, Form, UploadFile
from sqlalchemy.orm import Session

from app.database import get_db
from app.repositories.allergy_repository import AllergyRepository
from app.services.allergy_service import AllergyService
from app.services.image_processor import ImageProcessor


router = APIRouter(
    prefix="/validation",
    tags=["Validation"]
)


@router.post("/")
def validate_components(
    components: list[str] = Form(default=[]),
    image: UploadFile | None = File(default=None),
    db: Session = Depends(get_db)
):
    service = AllergyService(
        AllergyRepository(db)
    )

    image_text = ""

    if image and image.filename:
        image_processor = ImageProcessor(image.file)
        image_text = image_processor.process_image()

        if not image_text or "[ERRO]" in image_text.upper():
            return {
                "error": "Não foi possível processar a imagem ou extrair texto."
            }

    allergies = service.check_allergies(
        user_components=components,
        image_text=image_text
    )

    return {
        "allergies": allergies
    }