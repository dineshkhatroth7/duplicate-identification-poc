from database.models import Candidate
from app.logger import logger


def merge_candidates(db, existing_candidate, new_candidate):

    try:

        logger.info("Merging duplicate candidates")

        # Update missing or better fields

        if not existing_candidate.first_name:
            existing_candidate.first_name = new_candidate.get("first_name")

        if not existing_candidate.last_name:
            existing_candidate.last_name = new_candidate.get("last_name")

        if not existing_candidate.resume_text:
            existing_candidate.resume_text = new_candidate.get("resume_text")

        # Prefer latest resume if longer
        if new_candidate.get("resume_text"):

            if len(new_candidate.get("resume_text")) > len(existing_candidate.resume_text or ""):
                existing_candidate.resume_text = new_candidate.get("resume_text")

        db.commit()
        db.refresh(existing_candidate)

        logger.info(f"Candidate merged with ID {existing_candidate.id}")

        return existing_candidate

    except Exception as e:

        logger.error(f"Merge failed: {str(e)}")
        raise