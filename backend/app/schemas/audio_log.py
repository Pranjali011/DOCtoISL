from pydantic import BaseModel

class AudioLogResponse(BaseModel):
    id: int
    user_id: int
    text: str
    audio_path: str

    class Config:
        orm_mode = True
