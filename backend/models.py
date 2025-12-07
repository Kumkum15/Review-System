from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from .db import Base

class Submission(Base):
    __tablename__ = "submissions"

    id = Column(Integer, primary_key=True, index=True)
    rating = Column(Integer, nullable=False)
    review = Column(String, nullable=False)
    user_response = Column(String, nullable=True)
    summary = Column(String, nullable=True)
    actions = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
