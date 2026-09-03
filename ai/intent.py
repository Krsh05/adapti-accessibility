from google import genai
from google.genai import types
from dotenv import load_dotenv
import os
import json

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


def local_fallback(text):
    text = text.lower()

    if any(x in text for x in ["click", "where do i", "what do i do", "confusing"]):
        return {
            "intent": "request_guidance",
            "confidence": 0.70,
            "reason": "Local fallback detected a request for guidance"
        }

    if any(x in text for x in ["small text", "can't read", "cannot read", "font"]):
        return {
            "intent": "accessibility_help",
            "confidence": 0.75,
            "reason": "Local fallback detected a reading accessibility difficulty"
        }

    if any(x in text for x in ["simplify", "easier", "too much text"]):
        return {
            "intent": "simplify_content",
            "confidence": 0.75,
            "reason": "Local fallback detected a request to simplify content"
        }

    if any(x in text for x in ["apply", "application", "fill out", "form"]):
        return {
            "intent": "form_filling",
            "confidence": 0.75,
            "reason": "Local fallback detected a form-related request"
        }

    if any(x in text for x in ["language", "translate", "translation"]):
        return {
            "intent": "language_help",
            "confidence": 0.75,
            "reason": "Local fallback detected a language request"
        }

    return {
        "intent": "unknown",
        "confidence": 0.40,
        "reason": "No matching intent detected"
    }


def detect_intent(user_text):

    prompt = f"""
You are the AI intent detector for ADAPTI,
an accessibility platform.

Analyze what the user is trying to do.

Choose exactly ONE:

navigation
form_filling
reading
request_guidance
simplify_content
language_help
accessibility_help
unknown

User message:
{user_text}
"""

    try:
        response = client.models.generate_content(
            model="gemini-3.7-flash",
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema={
                    "type": "OBJECT",
                    "properties": {
                        "intent": {
                            "type": "STRING",
                            "enum": [
                                "navigation",
                                "form_filling",
                                "reading",
                                "request_guidance",
                                "simplify_content",
                                "language_help",
                                "accessibility_help",
                                "unknown"
                            ]
                        },
                        "confidence": {
                            "type": "NUMBER"
                        },
                        "reason": {
                            "type": "STRING"
                        }
                    },
                    "required": [
                        "intent",
                        "confidence",
                        "reason"
                    ]
                }
            )
        )

        return json.loads(response.text)

    except Exception as error:
        print(f"Gemini unavailable: {error}")
        print("Using local fallback...")

        return local_fallback(user_text)