import os
from google import genai

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def generate_interview_questions(role):
    prompt = f"""
Generate 5 interview questions for a {role}.
Return only the questions as a numbered list.
"""

    response = client.models.generate_content(
        model="gemini-3.5-flash",
        contents=prompt,
    )

    return response.text