from .connection import SessionLocal
from .models import CandidateStaging, CandidateMain


def insert_staging_candidate(data: dict):
    db = SessionLocal()
    try:
        candidate = CandidateStaging(**data)
        db.add(candidate)
        db.commit()
        db.refresh(candidate)
        return candidate
    finally:
        db.close()


def fetch_pending_candidates():
    db = SessionLocal()
    try:
        return db.query(CandidateStaging).filter(
            CandidateStaging.status == "PENDING"
        ).all()
    finally:
        db.close()