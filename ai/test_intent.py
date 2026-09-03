from intent import detect_intent

tests = [
    "I don't know where to click",
    "This page has way too much text",
    "I want to fill out this application",
    "Can you make this easier to understand?",
    "I can't read the small text",
    "I want to change the language"
]

for text in tests:
    result = detect_intent(text)

    print("\nUSER:", text)
    print("INTENT:", result["intent"])
    print("CONFIDENCE:", result["confidence"])
    print("REASON:", result["reason"])