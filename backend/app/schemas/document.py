from pydantic import BaseModel

class DocumentResponse(BaseModel):
    id: int
    user_id: int
    filename: str
    extracted_text: str

    class Config:
        orm_mode = True
