from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.summary import Summary
from app.models.document import Document

router = APIRouter(prefix="/history", tags=["History"])

@router.get("/{user_id}")
def get_history(user_id: int, db: Session = Depends(get_db)):
    histories = (
        db.query(Summary, Document)
        .join(Document, Summary.document_id == Document.id)
        .filter(Summary.user_id == user_id)
        .all()
    )

    result = []
    for summary, doc in histories:
        result.append({
            "summary_id": summary.id,
            "filename": doc.original_filename,
            "summary_text": summary.summary_text,
            "wordcloud": doc.wordcloud_path,
            "isl_video": summary.isl_video  
        })

    return result
