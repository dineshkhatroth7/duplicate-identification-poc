import json
from ai.claude_client import GeminiClient


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

NEW CANDIDATE:
{new_candidate}

POTENTIAL MATCHES:
{matches}

Return JSON format:

{{
"is_duplicate": true/false,
"confidence": 0.0-1.0
}}
"""

            return prompt

        except Exception as e:

            raise Exception(f"Prompt Build Error: {str(e)}")

    def verify(self, payload: dict):

        try:

            prompt = self.build_prompt(payload)

            response = self.ai.generate(prompt)

            parsed_response = json.loads(response)

            if "confidence" not in parsed_response:
                raise Exception("Invalid AI response format")

            return parsed_response

        except json.JSONDecodeError:

            raise Exception("AI returned invalid JSON")

        except Exception as e:

            raise Exception(f"Duplicate Verification Failed: {str(e)}")