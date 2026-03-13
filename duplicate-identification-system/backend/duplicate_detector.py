# backend/duplicate_detector.py

from database.candidate_repository import (
    get_candidate_by_id,
    get_candidate_by_email,
    get_candidate_by_phone
)

from database.duplicate_repository import create_duplicate_log
from backend.duplicate_score import calculate_duplicate_score
from vector_db.faiss_index import search_candidate
from ai.similarity_service import ai_duplicate_check
from app.logger import logger


DUPLICATE_HIGH_THRESHOLD = 90
DUPLICATE_POSSIBLE_THRESHOLD = 70


def detect_duplicates(candidate: dict, db) -> dict:

    try:

        explanation = []

        candidate_id = candidate.get("candidate_id")
        email = candidate.get("email", "").strip().lower()
        phone = candidate.get("phone", "").strip()

        id_match = False
        email_match = False
        phone_match = False
        vector_score = 0.0
        matched_candidate = None

        # ------------------------
        # ID check
        # ------------------------
        if candidate_id:

            existing = get_candidate_by_id(db, candidate_id)

            if existing:
                id_match = True
                matched_candidate = existing
                explanation.append("Candidate ID already exists")

        # ------------------------
        # Email check
        # ------------------------
        if email:

            existing = get_candidate_by_email(db, email)

            if existing:
                email_match = True
                matched_candidate = existing
                explanation.append("Email matched with existing candidate")

        # ------------------------
        # Phone check
        # ------------------------
        if phone:

            existing = get_candidate_by_phone(db, phone)

            if existing:
                phone_match = True
                matched_candidate = existing
                explanation.append("Phone number matched with existing candidate")

        # ------------------------
        # Vector similarity
        # ------------------------
        matches = search_candidate(candidate)

        if matches:

            try:
                vector_score = max(match["score"] for match in matches)
            except:
                vector_score = 0.85

            explanation.append(f"Resume similarity score: {round(vector_score,2)}")

        # ------------------------
        # Calculate score
        # ------------------------
        score = calculate_duplicate_score(
            email_match=email_match,
            phone_match=phone_match,
            vector_score=vector_score
        )

        # ------------------------
        # Decision Engine
        # ------------------------
        if id_match:
            status = "ID_DUPLICATE"

        elif score >= DUPLICATE_HIGH_THRESHOLD:
            status = "HIGH_DUPLICATE"

        elif score >= DUPLICATE_POSSIBLE_THRESHOLD:
            status = "POSSIBLE_DUPLICATE"

        else:
            status = "NEW"

        # ------------------------
        # AI verification
        # ------------------------
        ai_result = None

        if status in ["HIGH_DUPLICATE", "POSSIBLE_DUPLICATE"] and matched_candidate:

            logger.info("Running AI duplicate verification")

            ai_result = ai_duplicate_check(candidate, matched_candidate)

            if ai_result:

                explanation.append(
                    f"Nickname similarity: {round(ai_result['nickname_score'],2)}"
                )

                explanation.append(
                    f"Experience similarity: {round(ai_result['experience_score'],2)}"
                )

                explanation.append(
                    f"AI confidence score: {round(ai_result['ai_score'],2)}"
                )

        # ------------------------
        # Log duplicate
        # ------------------------
        if status != "NEW":

            log_data = {
                "candidate_id": candidate_id,
                "matched_candidate_id": matched_candidate.id if matched_candidate else None,
                "match_type": status,
                "confidence_score": score
            }

            create_duplicate_log(db, log_data)

        # ------------------------
        # Return result
        # ------------------------
        return {

            "status": status,

            "score": score,

            "signals": {
                "id_match": id_match,
                "email_match": email_match,
                "phone_match": phone_match,
                "semantic_similarity": vector_score
            },

            "ai_verification": ai_result,

            "explanation": explanation,

            "matched_candidate": matched_candidate

        }

    except Exception as e:

        logger.error(f"Duplicate detection failed: {str(e)}")
        raise