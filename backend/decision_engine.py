def make_decision(ai_result: dict, threshold: float = 0.75):
    """
    Decide whether candidate is duplicate, review, or unique
    based on AI confidence score.
    """

    try:

        if not isinstance(ai_result, dict):
            raise ValueError("Invalid AI result format")

        confidence = ai_result.get("confidence")

        if confidence is None:
            raise ValueError("AI result missing confidence score")

        if confidence >= threshold:

            return {
                "status": "DUPLICATE",
                "action": "AUTO_MERGE",
                "confidence": confidence
            }

        elif confidence >= 0.5:

            return {
                "status": "REVIEW",
                "action": "MANUAL_REVIEW",
                "confidence": confidence
            }

        else:

            return {
                "status": "UNIQUE",
                "action": "MOVE_TO_MAIN",
                "confidence": confidence
            }

    except Exception as e:

        raise Exception(f"Decision engine failed: {str(e)}")