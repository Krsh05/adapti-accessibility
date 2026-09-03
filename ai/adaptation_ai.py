from google import genai
from google.genai import types
from dotenv import load_dotenv
import os
import json

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


def local_fallback(text):
    text = text.lower()

    if any(x in text for x in [
        "small text",
        "text is small",
        "can't read",
        "cannot read",
        "hard to read"
    ]):
        return {
            "problem": "small_text",
            "action": "increase_font_size",
            "value": "large",
            "confidence": 0.75
        }

    if any(x in text for x in [
        "too much text",
        "too many words",
        "overwhelming"
    ]):
        return {
            "problem": "complex_content",
            "action": "simplify_content",
            "value": "simple",
            "confidence": 0.75
        }

    if any(x in text for x in [
        "too many buttons",
        "too many options",
        "cluttered"
    ]):
        return {
            "problem": "cluttered_interface",
            "action": "reduce_visual_clutter",
            "value": "minimal",
            "confidence": 0.75
        }

    if any(x in text for x in [
        "can't understand",
        "cannot understand",
        "confusing",
        "confused"
    ]):
        return {
            "problem": "confusing_interface",
            "action": "provide_guidance",
            "value": "step_by_step",
            "confidence": 0.70
        }

    if any(x in text for x in [
        "language",
        "translate",
        "translation"
    ]):
        return {
            "problem": "language_barrier",
            "action": "translate_content",
            "value": "user_language",
            "confidence": 0.75
        }

    return {
        "problem": "unknown",
        "action": "no_change",
        "value": "default",
        "confidence": 0.40
    }


def determine_adaptation(user_problem):

    prompt = f"""
You are the adaptation intelligence of ADAPTI.

ADAPTI is an accessibility system that changes digital
interfaces based on a user's difficulties.

Analyze the user's problem and decide what interface
adaptation should happen.

Possible problems:
- small_text
- complex_content
- cluttered_interface
- confusing_interface
- language_barrier
- navigation_difficulty
- unknown

Possible actions:
- increase_font_size
- simplify_content
- reduce_visual_clutter
- provide_guidance
- translate_content
- simplify_navigation
- no_change

User problem:
{user_problem}
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
                        "problem": {
                            "type": "STRING"
                        },
                        "action": {
                            "type": "STRING"
                        },
                        "value": {
                            "type": "STRING"
                        },
                        "confidence": {
                            "type": "NUMBER"
                        }
                    },
                    "required": [
                        "problem",
                        "action",
                        "value",
                        "confidence"
                    ]
                }
            )
        )

        return json.loads(response.text)

    except Exception as error:
        print("Gemini unavailable. Using local fallback.")
        return local_fallback(user_problem)