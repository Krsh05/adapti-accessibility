from adaptation_ai import determine_adaptation


tests = [
    "The text is too small and I can't read it",
    "There is way too much text on this page",
    "There are too many buttons and the page feels cluttered",
    "I don't understand what I am supposed to do",
    "I need this page in another language"
]


for text in tests:

    result = determine_adaptation(text)

    print("\nUSER:", text)
    print("PROBLEM:", result["problem"])
    print("ACTION:", result["action"])
    print("VALUE:", result["value"])
    print("CONFIDENCE:", result["confidence"])