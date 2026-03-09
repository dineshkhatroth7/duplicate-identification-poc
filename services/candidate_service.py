from database.connection import SessionLocal
from database.models import CandidateStaging
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException
from services.kafka_producer import publish_candidate


def get_staging_candidates():
    """
    Fetch candidates that need duplicate verification
    """

    db = SessionLocal()

    try:

        candidates = db.query(CandidateStaging).filter(
            CandidateStaging.status.in_(["PENDING", "DUPLICATE_REVIEW"])
        ).all()

        result = [
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

        return result

    except SQLAlchemyError as e:

        raise HTTPException(
            status_code=500,
            detail=f"Database error while fetching candidates: {str(e)}"
        )

    finally:

        db.close()


def send_for_ai(candidate_id: int):
    """
    Send candidate data to Kafka for AI duplicate verification
    """

    db = SessionLocal()

    try:

        candidate = db.query(CandidateStaging).filter(
            CandidateStaging.id == candidate_id
        ).first()

        if not candidate:

            raise HTTPException(
                status_code=404,
                detail="Candidate not found"
            )

        payload = {
            "id": candidate.id,
            "name": candidate.name,
            "email": candidate.email,
            "phone": candidate.phone,
            "experience": candidate.experience
        }

        publish_candidate(payload)

        return {
            "status": "success",
            "message": "Candidate sent for AI verification",
            "candidate_id": candidate.id
        }

    except HTTPException:
        raise

    except SQLAlchemyError as e:

        raise HTTPException(
            status_code=500,
            detail=f"Database error: {str(e)}"
        )

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=f"Failed to send candidate for AI verification: {str(e)}"
        )

    finally:

        db.close()