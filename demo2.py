"""Demo 2: Three questions in one call, plus the traffic-light decision.
Run:  python demo2.py

What this demo shows:
    1. Jev can answer SEVERAL questions about the same message in ONE call.
    2. Every answer comes with a probability (a number between 0 and 1).
    3. Our own code uses that probability to decide what to do next,
       like a traffic light: GREEN (go), YELLOW (go, but check), RED (stop, ask a human).
"""

# ---------------------------------------------------------------------------
# Imports
# ---------------------------------------------------------------------------

# Python's built-in "time" module, used as a stopwatch.
import time

# Reads the .env file so the program can find your TYPESAFE_API_KEY.
from dotenv import load_dotenv

# From the TypeSafe SDK:
#   Choice         -> Jev picks ONE option from a list (e.g. which team)
#   Noul           -> a yes/no question; Jev answers with a probability from 0 to 1
#                     (0 = definitely no, 1 = definitely yes, 0.5 = unsure)
#   TypeSafeClient -> the object that sends our requests to TypeSafe AI
from typesafe_sdk import Choice, Noul, TypeSafeClient

# ---------------------------------------------------------------------------
# Setup
# ---------------------------------------------------------------------------

# Load the values from the .env file into the environment (this is where the API key lives).
load_dotenv()  # loads TYPESAFE_API_KEY from the .env file

# Create the client. It finds TYPESAFE_API_KEY on its own.
client = TypeSafeClient()  # reads TYPESAFE_API_KEY automatically

# The customer message we want Jev to understand.
message = "I paid twice for the course. Please help."

# ---------------------------------------------------------------------------
# Ask Jev three questions in a single call
# ---------------------------------------------------------------------------

# Start the stopwatch.
start = time.perf_counter()

# One call to Jev, with three questions. All three answers come back together.
response = client.system_one(
    # The text Jev should read.
    state=message,
    # Our questions. The keys ("team", "frustrated", "urgent") are names we choose;
    # we use the same names later to read the answers.
    questions={
        # Question 1: which team? Jev must pick exactly one option.
        "team": Choice(
            # What we want decided, in plain English.
            instructions="Which team should handle this",
            # The allowed options: name on the left, helpful description on the right.
            criteria={
                "payments": "Money, fees or refund issues",
                "tech": "Login, app or video problems",
                "courses": "Questions about course content",
            },
        ),
        # Question 2: is the customer frustrated? Jev answers with a number from 0 to 1.
        "frustrated": Noul(instructions="The customer sounds frustrated or upset"),
        # Question 3: is it urgent? Also a number from 0 to 1.
        "urgent": Noul(instructions="This message needs action today"),
    },
)

# Stop the stopwatch and convert seconds to milliseconds.
ms = (time.perf_counter() - start) * 1000

# ---------------------------------------------------------------------------
# Print the answers
# ---------------------------------------------------------------------------

# Get the answer to the "team" question (we'll use it several times below).
team = response.answers["team"]

# Blank line for readability.
print()

# Show the chosen team and the confidence as a percentage (e.g. "payments (97% sure)").
print("Team        :", team.choice, f"({team.confidence:.0%} sure)")

# .noul is the 0-to-1 probability for a Noul question. ":.2f" shows 2 decimals (e.g. 0.81).
print(f"Frustrated  : {response.answers['frustrated'].noul:.2f}")

# Same for the "urgent" question.
print(f"Urgent      : {response.answers['urgent'].noul:.2f}")

# One call answered all three questions; show how long that single call took.
print(f"Time        : {ms:.0f} ms for all three answers")

# team.probabilities is a dictionary with a probability for EVERY option, not just the winner,
# e.g. {"payments": 0.97, "tech": 0.02, "courses": 0.01}.
# The part in {} is a "dict comprehension": it rebuilds the dictionary with each value
# rounded to 2 decimals so it is easier to read.
print("All options :", {k: round(v, 2) for k, v in team.probabilities.items()})

# ---------------------------------------------------------------------------
# The traffic light: Jev gives the number, your code makes the decision
# ---------------------------------------------------------------------------

# Store the confidence (0 to 1) in a short variable name "p" (for probability).
p = team.confidence

# Blank line before the decision.
print()

# 0.90 or more: Jev is very sure, so we can route the message automatically.
if p >= 0.90:
    print(f"GREEN  -> send straight to the {team.choice} team")
# Between 0.60 and 0.90: probably right, but a person should double-check.
elif p >= 0.60:
    print(f"YELLOW -> send to {team.choice}, but flag for a human to check")
# Below 0.60: Jev is not sure enough, so a person should decide.
else:
    print("RED    -> not sure, ask a human")

# These thresholds (0.90 and 0.60) are OUR business rules, not Jev's.
# You can change them to be stricter or looser for your own app.

# Final blank line.
print()
