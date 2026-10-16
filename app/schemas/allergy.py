from pydantic import BaseModel, Field


class BulkAllergyCreate(BaseModel):
    names: list[str] = Field(min_length=1, max_length=100)
