"""Demo 2: Three questions in one call, plus the traffic-light decision.
Run:  python demo2.py
"""
import time

from dotenv import load_dotenv
from typesafe_sdk import Choice, Noul, TypeSafeClient

load_dotenv()  # loads TYPESAFE_API_KEY from the .env file
client = TypeSafeClient()  # reads TYPESAFE_API_KEY automatically

message = "Anna, I paid twice for the course. Please help."

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
        "frustrated": Noul(instructions="The customer sounds frustrated or upset"),
        "urgent": Noul(instructions="This message needs action today"),
    },
)
ms = (time.perf_counter() - start) * 1000

team = response.answers["team"]
print()
print("Team        :", team.choice, f"({team.confidence:.0%} sure)")
print(f"Frustrated  : {response.answers['frustrated'].noul:.2f}")
print(f"Urgent      : {response.answers['urgent'].noul:.2f}")
print(f"Time        : {ms:.0f} ms for all three answers")
print("All options :", {k: round(v, 2) for k, v in team.probabilities.items()})

# The traffic signal: Jev gives the number, your code makes the decision.
p = team.confidence
print()
if p >= 0.90:
    print(f"GREEN  -> send straight to the {team.choice} team")
elif p >= 0.60:
    print(f"YELLOW -> send to {team.choice}, but flag for a human to check")
else:
    print("RED    -> not sure, ask a human")
print()
