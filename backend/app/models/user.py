from sqlalchemy import Column, Integer, String, DateTime, func
from app.database import Base
from sqlalchemy.orm import relationship



class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), nullable=False)
    email = Column(String(150), unique=True, index=True, nullable=False)
    password = Column(String(255), nullable=False)  # bcrypt hash fits in 60 chars
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    def __repr__(self):
        return f"<User id={self.id} email={self.email}>"
    
    # Relationships onetomany
    documents = relationship("Document", back_populates="user")
    summaries = relationship("Summary", back_populates="user")
    isl_videos = relationship("ISLVideo", back_populates="user")
    audio_logs = relationship("AudioLog", back_populates="user")