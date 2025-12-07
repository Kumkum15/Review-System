from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware

from .db import Base, engine, SessionLocal
from .models import Submission
from .ai_utils import generate_user_response, generate_summary, generate_actions

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Review System Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class SubmissionIn(BaseModel):
    rating: int
    review: str


@app.post("/submit")
def submit(payload: SubmissionIn, db: Session = Depends(get_db)):
    if not (1 <= payload.rating <= 5):
        raise HTTPException(status_code=400, detail="Rating must be between 1-5")

    user_response = generate_user_response(payload.rating, payload.review)
    summary = generate_summary(payload.review)
    actions = generate_actions(payload.rating, payload.review)

    item = Submission(
        rating=payload.rating,
        review=payload.review,
        user_response=user_response,
        summary=summary,
        actions=actions
    )

    db.add(item)
    db.commit()
    db.refresh(item)

    return {"message": "Review stored", "id": item.id}


@app.get("/submissions")
def list_submissions(db: Session = Depends(get_db)):
    rows = db.query(Submission).order_by(Submission.created_at.desc()).all()
    return rows


@app.get("/stats")
def stats(db: Session = Depends(get_db)):
    rows = db.query(Submission).all()
    total = len(rows)
    avg_rating = sum(r.rating for r in rows) / total if total else 0

    dist = {i: 0 for i in range(1, 6)}
    for r in rows:
        dist[r.rating] += 1

    return {"total": total, "average_rating": avg_rating, "distribution": dist}
