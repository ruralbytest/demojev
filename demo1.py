"""Demo 1: Which team gets this message?
Run:  python demo1.py
Needs: pip install -r requirements.txt, and TYPESAFE_API_KEY set in your .env file.
"""
import time

from dotenv import load_dotenv
from typesafe_sdk import Choice, TypeSafeClient

load_dotenv()  # loads TYPESAFE_API_KEY from the .env file
client = TypeSafeClient()  # reads TYPESAFE_API_KEY automatically

message = "Anna, I paid twice for the course. Please help."
# Swap to this for the second run on camera:
# message = "I cannot log in to the app."

start = time.perf_counter()
response = client.system_one(
    state=message,
    questions={
        "team": Choice(
            instructions="Which team should handle this",
            criteria={
                "payments": "Money, fees or refund issues",
                "tech": "Login, app or video problems",
                "courses": "Questions about course content",
            },
        ),
    },
)
ms = (time.perf_counter() - start) * 1000

team = response.answers["team"]
print()
print("Message    :", message)
print("Team       :", team.choice)
print(f"Confidence : {team.confidence:.0%}")
print(f"Time       : {ms:.0f} ms")
print()
