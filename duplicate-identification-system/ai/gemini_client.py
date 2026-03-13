import google.generativeai as genai

GEMINI_API_KEY = "AIzaSyDxbY3oBK868Gd6Vd-cj4SBIfgC9E2Fi_Q"

genai.configure(api_key=GEMINI_API_KEY)

model = genai.GenerativeModel("gemini-1.5-flash")


def verify_duplicate(candidate1, candidate2):

    prompt = f"""
You are an AI system that detects duplicate candidates in an ATS system.

Compare the following two candidates and decide if they represent the SAME person.

Candidate 1:
{candidate1}

Candidate 2:
{candidate2}

Return JSON:
{{
"is_duplicate": true or false,
"confidence": 0-100,
"reason": "short explanation"
}}
"""

    response = model.generate_content(prompt)

    return response.text