from sqlalchemy import Column, Integer, String, DateTime, Text
from datetime import datetime
from .db import Base

class Submission(Base):
    __tablename__ = "submissions"

    id = Column(Integer, primary_key=True, index=True)
    rating = Column(Integer, nullable=False)
    review = Column(Text, nullable=False)
    user_response = Column(Text, nullable=True)
    summary = Column(Text, nullable=True)
    actions = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
