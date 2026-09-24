"""Demo 3: Same complaint in English, Tanglish and Tamil script, plus one vague message.
Run:  python demo3_tamil.py
Windows tip: if Tamil shows as boxes, run  chcp 65001  first, or use the VS Code terminal.
"""
import time

from dotenv import load_dotenv
from typesafe_sdk import Choice, TypeSafeClient

load_dotenv()  # loads TYPESAFE_API_KEY from the .env file
client = TypeSafeClient()  # reads TYPESAFE_API_KEY automatically

questions = {
    "team": Choice(
        instructions="Which team should handle this",
        criteria={
            "payments": "Money, fees or refund issues",
            "tech": "Login, app or video problems",
            "courses": "Questions about course content",
        },
    ),
}

messages = [
    ("English", "I paid twice for the course. Please help."),
    ("Tanglish", "Course ku rendu thadava pay panniten, help pannunga."),
    ("Tamil", "கோர்ஸுக்கு ரெண்டு தடவை பணம் கட்டிட்டேன். உதவி பண்ணுங்க."),
    ("Vague", "Ok sir, will see and tell."),
]

print()
for label, text in messages:
    start = time.perf_counter()
    team = client.system_one(state=text, questions=questions).answers["team"]
    ms = (time.perf_counter() - start) * 1000
    print(f"{label:9} -> {team.choice:9} {team.confidence:5.0%} sure   {ms:4.0f} ms")
print()
