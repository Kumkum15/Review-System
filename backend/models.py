# backend/models.py

from sqlalchemy import Column, Integer, String, Text, DateTime, func
from .db import Base   # <— MUST import Base from db.py

class Submission(Base):
    __tablename__ = "submissions"

    id = Column(Integer, primary_key=True, index=True)
    rating = Column(Integer, nullable=False)
    review = Column(Text, nullable=False)
    user_response = Column(Text, nullable=True)
    summary = Column(Text, nullable=True)
    actions = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
