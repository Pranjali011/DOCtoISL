from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field

from app.database import get_db
from app.utils.video_generator import generate_isl_video
from app.models.isl_video import ISLVideo


router = APIRouter(prefix="/isl", tags=["ISL Video Generation"])


# Pydantic Schema
class ISLVideoRequest(BaseModel):
    user_id: int = Field(..., gt=0)
    sentences: list[str] = Field(..., min_length=1)


# Generate ISL Videos Route
@router.post("/generate", status_code=status.HTTP_201_CREATED)
def generate_isl_videos(
    payload: ISLVideoRequest,
    db: Session = Depends(get_db)
):
    """
    Convert simplified ISL-friendly sentences into video clips.
    Stores output video paths in the database.
    """

    user_id = payload.user_id
    sentences = payload.sentences

    video_paths = []

    for sentence in sentences:

        if not sentence.strip():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Blank sentence found in list."
            )

        # Generate video
        video_path = generate_isl_video(sentence)

        if not video_path:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to generate ISL video for: '{sentence}'"
            )

        video_paths.append(video_path)

        # Save in DB
        db_entry = ISLVideo(
            user_id=user_id,
            sentence=sentence,
            video_path=video_path
        )
        db.add(db_entry)

    db.commit()

    return {
        "message": "ISL videos generated successfully",
        "count": len(video_paths),
        "videos": video_paths
    }
