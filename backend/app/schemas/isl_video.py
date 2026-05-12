from pydantic import BaseModel

class ISLVideoResponse(BaseModel):
    id: int
    user_id: int
    sentence: str
    video_path: str

    class Config:
        orm_mode = True
