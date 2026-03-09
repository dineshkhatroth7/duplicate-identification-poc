from sqlalchemy.exc import SQLAlchemyError
from .connection import SessionLocal
from .models import CandidateMain, CandidateStaging


def merge_candidates(source_id: int, target_id: int):

    db = SessionLocal()

    try:

        source = db.query(CandidateStaging).filter_by(id=source_id).first()
        target = db.query(CandidateMain).filter_by(id=target_id).first()

        if not source:
            raise ValueError(f"Source candidate {source_id} not found")

        if not target:
            raise ValueError(f"Target candidate {target_id} not found")

        # merge fields
        target.name = target.name or source.name
        target.email = target.email or source.email
        target.phone = target.phone or source.phone
        target.experience = target.experience or source.experience

        db.delete(source)

        db.commit()

        return {
            "status": "success",
            "message": "Merge successful"
        }

    except SQLAlchemyError as e:

        db.rollback()

        raise Exception(f"Database merge failed: {str(e)}")

    except Exception as e:

        db.rollback()

        raise e

    finally:

        db.close()