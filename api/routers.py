from fastapi import APIRouter, HTTPException
from services.candidate_service import get_staging_candidates, send_for_ai

from ai.verifier import DuplicateVerifier
from ai.confidence_scoring import ConfidenceScorer

router = APIRouter(
    prefix="/duplicate_candidate_detection",
    tags=["Duplicate Candidate Detection"]
)


verifier = DuplicateVerifier()
scorer = ConfidenceScorer()


@router.get("/")
def health_check():
    """
    Health check endpoint
    """

    return {
        "status": "success",
        "message": "Duplicate Candidate Detection API is running"
    }


@router.get("/candidates/staging")
def read_staging_candidates():
    """
    Fetch candidates from staging table
    """

    try:
        candidates = get_staging_candidates()

        if not candidates:
            return {
                "status": "success",
                "count": 0,
                "message": "No staging candidates found",
                "data": []
            }

        return {
            "status": "success",
            "count": len(candidates),
            "data": candidates
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error fetching staging candidates: {str(e)}"
        )


@router.post("/candidates/{candidate_id}/verify")
def verify_candidate(candidate_id: int):
    """
    Send candidate to AI verification (POC-2 Duplicate Identification)
    """

    try:
        result = send_for_ai(candidate_id)

        if not result:
            raise HTTPException(
                status_code=404,
                detail="Candidate not found in staging"
            )

        return {
            "status": "success",
            "candidate_id": candidate_id,
            "verification_result": result
        }

    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"AI verification failed: {str(e)}"
        )


@router.post("/duplicate-check")
async def duplicate_check(payload: dict):
    """
    Duplicate Identification API
    """

    try:
        # -------- Step 1: Validate Input --------
        if "new_candidate" not in payload:
            raise ValueError("new_candidate missing")

        if "potential_matches_from_db" not in payload:
            raise ValueError("potential_matches_from_db missing")

        threshold = payload.get("threshold", 0.75)

        # -------- Step 2: AI Verification --------
        ai_result = verifier.verify(payload)

        # -------- Step 3: Confidence Scoring --------
        result = scorer.evaluate(ai_result)

        # -------- Step 4: Final Decision --------
        status = result["status"]

        final_action = {}

        if status == "UNIQUE":

            final_action = {
                "action_taken": "MOVED_TO_MAIN",
                "staging_status": "COMPLETED",
                "moved_to_main": True
            }

        elif status == "DUPLICATE":

            final_action = {
                "action_taken": "AUTO_MERGE",
                "staging_status": "DUPLICATE_FOUND",
                "moved_to_main": False
            }

        else:

            final_action = {
                "action_taken": "MANUAL_REVIEW",
                "staging_status": "AWAITING_HR_REVIEW",
                "moved_to_main": False
            }

        return {
            "ai_result": ai_result,
            "evaluation": result,
            "final_action": final_action
        }

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Duplicate check failed: {str(e)}")