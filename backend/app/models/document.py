from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base


class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)

    # User who uploaded the document
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    # Keep original filename exactly as user uploaded
    original_filename = Column(String(255), nullable=False)

    # Optional: store saved filename (if you store file in /uploads)
    saved_filename = Column(String(255), nullable=True)

    # Extracted text from file
    extracted_text = Column(Text, nullable=False)

    # Wordcloud image path
    wordcloud_path = Column(String(255), nullable=True)

    # Timestamp
    uploaded_at = Column(DateTime, default=datetime.utcnow)

    # Relationship
    user = relationship("User", back_populates="documents")
    summaries = relationship("Summary", back_populates="document")
