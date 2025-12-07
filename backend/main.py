from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from .db import SessionLocal, engine, Base
from .models import Submission
from .ai_utils import call_gemini
from fastapi.middleware.cors import CORSMiddleware

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Review System Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # for prod, restrict origins
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

class SubmissionOut(BaseModel):
    id: int
    rating: int
    review: str
    user_response: str
    summary: str
    actions: str
    created_at: str

    class Config:
        orm_mode = True

@app.post("/submit", response_model=SubmissionOut)
def submit(payload: SubmissionIn, db: Session = Depends(get_db)):
    if not (1 <= payload.rating <= 5):
        raise HTTPException(status_code=400, detail="rating must be 1-5")

    item = Submission(
        rating=payload.rating,
        review=payload.review,
    )
    db.add(item)
    db.commit()
    db.refresh(item)

    return SubmissionOut(
        id=item.id,
        rating=item.rating,
        review=item.review,
        user_response=item.user_response,
        summary=item.summary,
        actions=item.actions,
        created_at=item.created_at.isoformat(),
    )

@app.get("/submissions")
def list_submissions(db: Session = Depends(get_db)):
    rows = db.query(Submission).order_by(Submission.created_at.desc()).all()
    return [
        {
            "id": r.id,
            "rating": r.rating,
            "review": r.review,
            "user_response": r.user_response,
            "summary": r.summary,
            "actions": r.actions,
            "created_at": r.created_at.isoformat(),
        }
        for r in rows
    ]

@app.get("/stats")
def stats(db: Session = Depends(get_db)):
    rows = db.query(Submission).all()
    total = len(rows)
    avg_rating = float(sum(r.rating for r in rows) / total) if total else 0.0
    dist = {str(i): 0 for i in range(1, 6)}
    for r in rows:
        dist[str(r.rating)] += 1
    return {"total": total, "average_rating": avg_rating, "distribution": dist}

# Uvicorn agnostic start if run as script (Render uses uvicorn)
if __name__ == "__main__":
    import uvicorn, os
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("backend.main:app", host="0.0.0.0", port=port)
