from sqlalchemy import Column, Integer, String, DateTime, func
from .db import Base

class Submission(Base):
    __tablename__ = "submissions"
    id = Column(Integer, primary_key=True, index=True)
    rating = Column(Integer, nullable=False)
    review = Column(String, nullable=False)
    user_response = Column(String, nullable=False, default="")
    summary = Column(String, nullable=False, default="")
    actions = Column(String, nullable=False, default="")
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
