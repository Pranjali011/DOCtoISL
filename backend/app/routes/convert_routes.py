import os
from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field

from app.database import get_db
from app.models.summary import Summary
from app.models.document import Document

from app.utils.summarizer import (
    generate_summary,
    split_into_sentences,
    simplify_sentence
)

from app.utils.isl_converter import sentence_to_isl


router = APIRouter(prefix="/convert", tags=["Text Conversion"])


# ---- Schemas ----
class TextToISLRequest(BaseModel):
    user_id: int = Field(..., gt=0)
    document_id: int | None = None      # <-- allow None
    text: str = Field(..., min_length=3)


class SummaryToISLRequest(BaseModel):
    summary_id: int = Field(..., gt=0)


# 1️ TEXT → SUMMARY → ISL
@router.post("/text-to-isl")
def convert_text_to_isl(payload: TextToISLRequest, db: Session = Depends(get_db)):

    user_id = payload.user_id
    document_id = payload.document_id
    text = payload.text.strip()

    # Validate document only if provided
    if document_id:
        doc = db.query(Document).filter(Document.id == document_id).first()
        if not doc:
            raise HTTPException(404, "Document not found.")

    # STEP 1: Generate summary
    summary_text = generate_summary(text)

    # STEP 2: Simplify sentences
    raw_sentences = split_into_sentences(summary_text)
    simplified_sentences = [simplify_sentence(s) for s in raw_sentences]

    # STEP 3: Convert to ISL videos
    isl_output = []
    for s in simplified_sentences:
        result = sentence_to_isl(s)
        isl_output.append(result)

    # STEP 4: Choose first usable video for preview
    first_video_local = next(
        (item.get("video_path") for item in isl_output if item.get("video_path")),
        None
    )

    video_url = None
    if first_video_local:
        filename = os.path.basename(first_video_local)
        video_url = f"/convert/video/{filename}"

    # STEP 5: Save summary in DB
    summary_entry = Summary(
        user_id=user_id,
        document_id=document_id,   
        summary_text=summary_text,
        video_path=first_video_local
    )

    db.add(summary_entry)
    db.commit()
    db.refresh(summary_entry)

    return {
        "message": "Conversion Completed",
        "summary_id": summary_entry.id,
        "summary_text": summary_text,
        "simplified_sentences": simplified_sentences,
        "isl_output": isl_output,
        "video_url": video_url
    }


# 2️⃣ SUMMARY → ISL AGAIN
@router.post("/summary-to-isl")
def summary_to_isl_route(payload: SummaryToISLRequest, db: Session = Depends(get_db)):

    summary_obj = db.query(Summary).filter(Summary.id == payload.summary_id).first()
    if not summary_obj:
        raise HTTPException(404, "Summary not found.")

    summary_text = summary_obj.summary_text
    raw = split_into_sentences(summary_text)
    simplified = [simplify_sentence(s) for s in raw]
    isl_output = [sentence_to_isl(s) for s in simplified]

    return {
        "message": "ISL conversion successful",
        "summary_id": payload.summary_id,
        "summary_text": summary_text,
        "simplified_sentences": simplified,
        "isl_output": isl_output
    }


# 3️⃣ SERVE VIDEO FROM /generated_videos/
@router.get("/video/{filename}")
def get_isl_video(filename: str):

    file_path = os.path.join(os.getcwd(), "generated_videos", filename)

    if not os.path.exists(file_path):
        raise HTTPException(404, "Video not found")

    return FileResponse(file_path, media_type="video/mp4")
