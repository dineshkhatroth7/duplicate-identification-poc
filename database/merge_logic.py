from sqlalchemy.exc import SQLAlchemyError
from .connection import SessionLocal
from .models import CandidateMain, CandidateStaging


def merge_candidates(source_id: int, target_id: int):
    db = SessionLocal()

    try:
        source = db.query(CandidateStaging).filter_by(id=source_id).first()
        target = db.query(CandidateMain).filter_by(id=target_id).first()

        if not source or not target:
            return "Candidate not found"

        target.name = target.name or source.name
        target.email = target.email or source.email
        target.phone = target.phone or source.phone
        target.experience = target.experience or source.experience

        db.delete(source)

        db.commit()

        return "Merge successful"

    except SQLAlchemyError as e:
        db.rollback()
        return f"Merge failed: {str(e)}"

    finally:
        db.close()