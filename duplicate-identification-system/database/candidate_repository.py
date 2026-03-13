from sqlalchemy.orm import Session
from database.models import Candidate


# Create new candidate
def create_candidate(db: Session, candidate_data: dict):

    candidate = Candidate(
        candidate_id=candidate_data.get("candidate_id"),
        first_name=candidate_data.get("first_name"),
        last_name=candidate_data.get("last_name"),
        email=candidate_data.get("email"),
        phone=candidate_data.get("phone"),
        resume_text=candidate_data.get("resume_text"),
    )

    db.add(candidate)
    db.commit()
    db.refresh(candidate)

    return candidate


# Get candidate by email
def get_candidate_by_email(db: Session, email: str):

    return db.query(Candidate).filter(Candidate.email == email).first()


# Get candidate by phone
def get_candidate_by_phone(db: Session, phone: str):

    return db.query(Candidate).filter(Candidate.phone == phone).first()


# Get candidate by id
def get_candidate_by_id(db: Session, candidate_id: int):

    return db.query(Candidate).filter(Candidate.id == candidate_id).first()