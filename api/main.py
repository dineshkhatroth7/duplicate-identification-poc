from fastapi import FastAPI
from services.candidate_service import get_staging_candidates, send_for_ai
app = FastAPI(title="Duplicate Candidate Detection")

@app.get("/candidates/staging")
def read_staging_candidates():
    """
    Fetch candidates from staging table
    """
    candidates = get_staging_candidates()

    return {
        "count": len(candidates),
        "data": candidates
    }


@app.post("/candidates/{candidate_id}/verify")
def verify_candidate(candidate_id: int):
    """
    Send candidate to AI verification
    """

    result = send_for_ai(candidate_id)

    return result

@app.get("/")
def health_check():
    return {"status": "API is running"}