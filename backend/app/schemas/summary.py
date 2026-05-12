from pydantic import BaseModel

class SummaryResponse(BaseModel):
    id: int
    user_id: int
    document_id: int
    summary_text: str

    class Config:
        orm_mode = True
