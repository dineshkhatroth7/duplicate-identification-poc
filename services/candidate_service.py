from database.connection import SessionLocal
from fastapi import HTTPException
from database.models import CandidateStaging
from .kafka_producer import publish_candidate


def get_staging_candidates():
    
    db = SessionLocal()

    try:

        candidates = db.query(CandidateStaging).filter(
            CandidateStaging.status.in_(["PENDING", "DUPLICATE_REVIEW"])
        ).all()

        return [
            {
                "id": c.id,
                "name": c.name,
                "email": c.email,
                "phone": c.phone,
                "experience": c.experience,
                "status": c.status
            }
            for c in candidates
        ]

    finally:
        db.close()


def send_for_ai(candidate_id):

    db = SessionLocal()

    try:

        candidate = db.query(CandidateStaging).filter(
            CandidateStaging.id == candidate_id
        ).first()

        if not candidate:
         raise HTTPException(status_code=404, detail="Candidate not found")

        payload = {
            "id": candidate.id,
            "name": candidate.name,
            "email": candidate.email,
            "phone": candidate.phone,
            "experience": candidate.experience
        }

        publish_candidate(payload)

        return {
            "message": "Candidate sent for AI verification",
            "candidate_id": candidate.id
        }

    finally:
        db.close()