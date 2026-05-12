from fastapi import APIRouter, UploadFile, File, HTTPException, Depends, status
from sqlalchemy.orm import Session
import os

from app.database import get_db
from app.models.document import Document
from app.utils.pdf_reader import extract_text_from_pdf
from app.utils.docx_reader import extract_text_from_docx
from app.utils.ocr import extract_text_from_image
from app.utils.wordcloud_gen import generate_wordcloud

router = APIRouter(prefix="/document", tags=["Document Processing"])


# 1️ UPLOAD DOCUMENT + EXTRACT TEXT + GENERATE WORDCLOUD
@router.post("/upload")
async def upload_document(
    user_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    filename = file.filename.lower()
    allowed = (".pdf", ".docx", ".jpg", ".jpeg", ".png")

    if not filename.endswith(allowed):
        raise HTTPException(
            status_code=400,
            detail="Unsupported file type. Allowed: PDF, DOCX, JPG, PNG"
        )

    file_bytes = await file.read()
    extracted_text = ""

    # --- Extract text ---
    if filename.endswith(".pdf"):
        extracted_text = extract_text_from_pdf(file_bytes)
    elif filename.endswith(".docx"):
        extracted_text = extract_text_from_docx(file_bytes)
    else:
        extracted_text = extract_text_from_image(file_bytes)

    if not extracted_text.strip():
        raise HTTPException(400, "No readable text found in document.")

    # --- Generate Word Cloud ---
    try:
        wordcloud_path = generate_wordcloud(extracted_text)
    except Exception as e:
        raise HTTPException(500, f"Wordcloud generation failed: {str(e)}")

    # --- Save to database ---
    new_doc = Document(
        user_id=user_id,
        original_filename=filename,
        saved_filename=filename,
        extracted_text=extracted_text,
        wordcloud_path=wordcloud_path
    )

    db.add(new_doc)
    db.commit()
    db.refresh(new_doc)

    return {
        "message": "Document uploaded successfully",
        "document_id": new_doc.id,
        "filename": new_doc.original_filename,
        "text": new_doc.extracted_text,
        "wordcloud": new_doc.wordcloud_path
    }


# 2️ GET ALL DOCUMENTS FOR A USER
@router.get("/{user_id}")
def get_user_documents(user_id: int, db: Session = Depends(get_db)):
    docs = (
        db.query(Document)
        .filter(Document.user_id == user_id)
        .order_by(Document.id.desc())
        .all()
    )

    return {"documents": docs}


# 3️ DELETE A DOCUMENT
@router.delete("/delete/{doc_id}")
def delete_document(doc_id: int, db: Session = Depends(get_db)):
    doc = db.query(Document).filter(Document.id == doc_id).first()

    if not doc:
        raise HTTPException(404, "Document not found")

    # Optional: delete stored wordcloud file
    if doc.wordcloud_path and os.path.exists(doc.wordcloud_path):
        try:
            os.remove(doc.wordcloud_path)
        except:
            pass  # do not break deletion if file can't be removed

    db.delete(doc)
    db.commit()

    return {"message": "Document deleted successfully", "deleted_id": doc_id}
