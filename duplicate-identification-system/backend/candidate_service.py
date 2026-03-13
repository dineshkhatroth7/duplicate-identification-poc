from backend.duplicate_detector import detect_duplicates
from backend.candidate_merge import merge_candidates

from database.candidate_repository import create_candidate
from vector_db.faiss_index import add_candidate
from app.logger import logger


def process_candidate(candidate: dict, db):

    """
    Main candidate processing pipeline.

    Flow:
    1️⃣ Detect duplicates
    2️⃣ If NEW → store candidate
    3️⃣ If DUPLICATE → merge candidate
    """

    try:

        logger.info("Processing candidate")

        result = detect_duplicates(candidate, db)

        status = result.get("status")
        score = result.get("score")
        ai_result = result.get("ai_verification")
        explanation = result.get("explanation")
        matched_candidate = result.get("matched_candidate")

        # -----------------------------
        # NEW Candidate
        # -----------------------------
        if status == "NEW":

            new_candidate = create_candidate(db, candidate)

            add_candidate(candidate)

            logger.info(f"New candidate stored: {new_candidate.id}")

            return {
                "status": "NEW_CANDIDATE",
                "candidate_id": new_candidate.id,
                "duplicate_score": score,
                "ai_verification": ai_result,
                "explanation": explanation
            }

        # -----------------------------
        # DUPLICATE → MERGE
        # -----------------------------
        if matched_candidate:

            logger.info("Merging duplicate candidates")

            merged_candidate = merge_candidates(
                db,
                matched_candidate,
                candidate
            )

            logger.info(
                f"Candidate merged with existing ID {merged_candidate.id}"
            )

            return {
                "status": "MERGED",
                "candidate_id": merged_candidate.id,
                "duplicate_score": score,
                "ai_verification": ai_result,
                "explanation": explanation,
                "message": "Duplicate candidate merged successfully"
            }

        return result

    except Exception as e:

        logger.error(f"Candidate processing error: {str(e)}")
        raise