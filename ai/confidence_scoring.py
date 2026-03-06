class ConfidenceScorer:

    def __init__(self, threshold=0.75):
        self.threshold = threshold

    def evaluate(self, ai_result: dict):

        try:
            confidence = ai_result.get("confidence", 0)

            if confidence >= self.threshold:
                status = "DUPLICATE"

            elif 0.50 <= confidence < self.threshold:
                status = "MANUAL_REVIEW"

            else:
                status = "UNIQUE"

            return {
                "status": status,
                "confidence": confidence,
                "recommendation": ai_result.get("recommendation"),
                "matched_profile": ai_result.get("matched_profile"),
                "match_evidence": ai_result.get("match_evidence")
            }

        except Exception as e:
            raise Exception(f"Confidence Scoring Failed: {str(e)}") 
