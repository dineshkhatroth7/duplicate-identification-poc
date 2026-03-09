from ai.verifier import DuplicateVerifier
from ai.confidence_scoring import ConfidenceScorer
from backend.decision_engine import make_decision


verifier = DuplicateVerifier()
scorer = ConfidenceScorer()


def run_duplicate_pipeline(payload: dict):
    """
    Main pipeline for duplicate detection
    """

    try:

        # -----------------------------
        # Step 1: Validate Input
        # -----------------------------
        if not isinstance(payload, dict):
            raise ValueError("Payload must be a dictionary")

        if "new_candidate" not in payload:
            raise ValueError("new_candidate missing")

        if "potential_matches_from_db" not in payload:
            raise ValueError("potential_matches_from_db missing")

        threshold = payload.get("threshold", 0.75)

        # -----------------------------
        # Step 2: AI Verification
        # -----------------------------
        ai_result = verifier.verify(payload)

        if not ai_result:
            raise Exception("AI verification returned empty result")

        # -----------------------------
        # Step 3: Confidence Scoring
        # -----------------------------
        evaluation = scorer.evaluate(ai_result)

        if "status" not in evaluation:
            raise Exception("Confidence scoring returned invalid result")

        # -----------------------------
        # Step 4: Decision Engine
        # -----------------------------
        decision = make_decision(ai_result, threshold)

        return {
            "pipeline_status": "success",
            "ai_result": ai_result,
            "evaluation": evaluation,
            "decision": decision
        }

    except ValueError as e:

        raise ValueError(f"Pipeline validation error: {str(e)}")

    except Exception as e:

        raise Exception(f"Duplicate pipeline failed: {str(e)}")