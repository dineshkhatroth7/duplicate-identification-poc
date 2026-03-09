from sqlalchemy.exc import SQLAlchemyError
from .connection import SessionLocal
from .models import CandidateStaging


def insert_staging_candidate(data: dict):

    db = SessionLocal()

    try:

        candidate = CandidateStaging(**data)

        db.add(candidate)
        db.commit()
        db.refresh(candidate)

        return candidate

    except SQLAlchemyError as e:

        db.rollback()

        raise Exception(f"Database insert failed: {str(e)}")

    finally:

        db.close()


def fetch_pending_candidates():

    db = SessionLocal()

    try:

        candidates = db.query(CandidateStaging).filter(
            CandidateStaging.status == "PENDING"
        ).all()

        return candidates

    except SQLAlchemyError as e:

        raise Exception(f"Database fetch failed: {str(e)}")

    finally:

        db.close()