from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field

from app.database import get_db
from app.models.audio_log import AudioLog
from app.utils.tts import generate_speech_audio


router = APIRouter(prefix="/tts", tags=["Text-to-Speech"])


# Pydantic Request Schema
class TTSRequest(BaseModel):
    user_id: int = Field(..., gt=0)
    text: str = Field(..., min_length=1)


# Text → Speech Route
@router.post("/speak", status_code=status.HTTP_201_CREATED)
def text_to_speech(
    payload: TTSRequest,
    db: Session = Depends(get_db)
):
    """
    Converts text into speech audio (MP3/WAV)
    Stores output path in database.
    """

    user_id = payload.user_id
    text = payload.text.strip()

    if not text:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Text cannot be empty."
        )

    # Generate speech audio file
    audio_path = generate_speech_audio(text)

    if not audio_path:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to generate speech audio."
        )

    # Save audio entry in DB
    db_entry = AudioLog(
        user_id=user_id,
        text=text,
        audio_path=audio_path
    )

    db.add(db_entry)
    db.commit()
    db.refresh(db_entry)

    # Response
    return {
        "message": "Audio generated successfully",
        "audio_id": db_entry.id,
        "audio_path": audio_path
    }
