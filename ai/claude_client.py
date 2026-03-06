# ------------------ Gemini API ------------------

import google.generativeai as genai
from config.settings import GEMINI_API_KEY


class GeminiClient:
    """
    LLM Client for Duplicate Identification (POC 2)
    """

    def __init__(self):
        try:
            genai.configure(api_key=GEMINI_API_KEY)
            self.model = genai.GenerativeModel("gemini-1.5-flash")
        except Exception as e:
            raise Exception(f"AI Model Initialization Failed: {str(e)}")

    def generate(self, prompt: str):

        try:
            response = self.model.generate_content(prompt)
            text = response.text.strip()

            return text

        except Exception as e:
            raise Exception(f"AI Generation Error: {str(e)}")



# ------------------ Groq API ------------------
from groq import Groq
from config.settings import GROQ_API_KEY


class GroqClient:
    """
    Client wrapper for Groq API
    """

    def __init__(self):
        self.client = Groq(api_key=GROQ_API_KEY)
        self.model = "llama-3.1-8b-instant"

    def generate(self, prompt: str) -> str:

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0
            )

            return response.choices[0].message.content

        except Exception as e:
            print(f"Groq API Error: {e}")
            return ""