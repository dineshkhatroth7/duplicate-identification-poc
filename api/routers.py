from fastapi import APIRouter, HTTPException
from services.candidate_service import get_staging_candidates
from backend.duplicate_pipeline import run_duplicate_pipeline

router = APIRouter(
    prefix="/duplicate_candidate_detection",
    tags=["Duplicate Candidate Detection"]
)


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


@router.post("/duplicate-check")
async def duplicate_check(payload: dict):
    """
    Duplicate detection endpoint
    """

    try:

        # Validate request
        if "new_candidate" not in payload:
            raise HTTPException(
                status_code=400,
                detail="new_candidate missing in payload"
            )

        if "potential_matches_from_db" not in payload:
            raise HTTPException(
                status_code=400,
                detail="potential_matches_from_db missing in payload"
            )

        # Run duplicate detection pipeline
        result = run_duplicate_pipeline(payload)

        return {
            "status": "success",
            "data": result
        }

    except HTTPException:
        raise

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=f"Duplicate detection failed: {str(e)}"
        )