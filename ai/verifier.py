 
import json
from ai.claude_client import GeminiClient, GroqClient


class DuplicateVerifier:

    def __init__(self):
        try:
            self.ai = GeminiClient()
        except Exception as e:
            raise Exception(f"Verifier Initialization Error: {str(e)}")

    def build_prompt(self, payload: dict):

        try:
            new_candidate = json.dumps(payload["new_candidate"], indent=2)
            matches = json.dumps(payload["potential_matches_from_db"], indent=2)

            prompt = f"""
You are an AI system responsible for detecting duplicate candidate profiles.

Analyze the NEW candidate and compare with POTENTIAL MATCHES.

NEW CANDIDATE:
{new_candidate}

POTENTIAL MATCHES:
{matches}

Rules:
- Detect semantic name matches (Bob = Robert)
- Compare phone/email
- Compare experience timeline
- Compare education

Return STRICT JSON format:

{{
"is_duplicate": true/false,
"confidence": 0.0-1.0,
"matched_profile": {{
"candidate_id": "",
"name": "",
"email": "",
"phone": ""
}},
"match_evidence": {{
"name_match": {{"score": 0.0,"detail": ""}},
"phone_match": {{"score": 0.0,"detail": ""}},
"experience_match": {{"score": 0.0,"detail": ""}},
"education_match": {{"score": 0.0,"detail": ""}}
}},
"recommendation": "MERGE_PROFILES | PROCEED | MANUAL_REVIEW"
}}
"""

            return prompt

        except Exception as e:
            raise Exception(f"Prompt Build Error: {str(e)}")

    def verify(self, payload: dict):

        try:
            prompt = self.build_prompt(payload)

            response = self.ai.generate(prompt)

            return json.loads(response)

        except json.JSONDecodeError:
            raise Exception("AI returned invalid JSON")

        except Exception as e:
            raise Exception(f"Duplicate Verification Failed: {str(e)}")