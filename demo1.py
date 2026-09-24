"""Demo 1: Which team gets this message?
Run:  python demo1.py
Needs: pip install -r requirements.txt, and TYPESAFE_API_KEY set in your .env file.

What this demo shows:
    We give Jev (TypeSafe AI's System One model) one customer message and ask
    ONE question: "Which team should handle this?" Jev picks one of three teams
    and tells us how confident it is. We also measure how fast the answer came back.
"""

# ---------------------------------------------------------------------------
# Imports: bring in the tools this script needs
# ---------------------------------------------------------------------------

# "time" is part of Python itself. We use it to measure how long Jev takes to answer.
import time

# "load_dotenv" comes from the python-dotenv package.
# It reads the .env file in this folder and puts each line (like TYPESAFE_API_KEY=...)
# into the environment variables, so the program can see your API key
# without the key ever being typed into the code.
from dotenv import load_dotenv

# From the TypeSafe SDK we import:
#   Choice         -> a question type where Jev must pick ONE option from a list
#   TypeSafeClient -> the object that talks to the TypeSafe AI servers for us
from typesafe_sdk import Choice, TypeSafeClient

# ---------------------------------------------------------------------------
# Setup: load the API key and create the client
# ---------------------------------------------------------------------------

# Read the .env file now. After this line, TYPESAFE_API_KEY is available to the program.
# This MUST run before we create the client, otherwise the client will not find the key.
load_dotenv()  # loads TYPESAFE_API_KEY from the .env file

# Create the client. It looks up TYPESAFE_API_KEY by itself, so we don't pass the key here.
client = TypeSafeClient()  # reads TYPESAFE_API_KEY automatically

# ---------------------------------------------------------------------------
# Input: the customer message we want Jev to read
# ---------------------------------------------------------------------------

# This is the text a customer sent us. In a real app this would come from email, chat, etc.
message = "Anna, I paid twice for the course. Please help."
# Swap to this for the second run on camera:
# message = "I cannot log in to the app."
# (To try it: put a "#" in front of the first message line and remove the "#" from this one.)

# ---------------------------------------------------------------------------
# Ask Jev: send the message and our question in a single call
# ---------------------------------------------------------------------------

# Note the exact time just before the call so we can work out how long it took.
# perf_counter() is a very precise stopwatch, measured in seconds.
start = time.perf_counter()

# system_one(...) sends our request to Jev and waits for the answer.
response = client.system_one(
    # "state" is the information Jev should look at, here the customer's message.
    state=message,
    # "questions" is a dictionary: each key is a name WE choose, each value is a question.
    # We can ask many questions at once (see demo2.py); here we ask just one called "team".
    questions={
        # "team" is a Choice question: Jev must pick exactly one of the options below.
        "team": Choice(
            # "instructions" tells Jev, in plain English, what we want decided.
            instructions="Which team should handle this",
            # "criteria" lists the allowed answers.
            # Left side  = the option name our code will get back.
            # Right side = a short description that helps Jev understand each option.
            criteria={
                "payments": "Money, fees or refund issues",
                "tech": "Login, app or video problems",
                "courses": "Questions about course content",
            },
        ),
    },
)

# Stop the stopwatch: (now - start) is in seconds, so multiply by 1000 to get milliseconds.
ms = (time.perf_counter() - start) * 1000

# ---------------------------------------------------------------------------
# Output: read Jev's answer and print it
# ---------------------------------------------------------------------------

# response.answers is a dictionary keyed by the question names we used above.
# We asked a question called "team", so we read that answer here.
team = response.answers["team"]

# Print an empty line so the output is easier to read.
print()

# Show the message we sent, so the viewer knows what Jev was reading.
print("Message    :", message)

# team.choice is the option Jev picked, for example "payments".
print("Team       :", team.choice)

# team.confidence is a number from 0 to 1 (e.g. 0.97).
# The ":.0%" format turns it into a percentage with no decimals (e.g. "97%").
print(f"Confidence : {team.confidence:.0%}")

# ":.0f" prints the milliseconds as a whole number (e.g. "312").
print(f"Time       : {ms:.0f} ms")

# One more empty line at the end for neat output.
print()
