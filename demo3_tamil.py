"""Demo 3: Same complaint in English, Tanglish and Tamil script, plus one vague message.
Run:  python demo3_tamil.py
Windows tip: if Tamil shows as boxes, run  chcp 65001  first, or use the VS Code terminal.

What this demo shows:
    1. Jev understands the same meaning in different languages and scripts.
       The "I paid twice" complaint should go to "payments" every time.
    2. When a message is vague, Jev's confidence drops, which tells us to ask a human.
"""

# ---------------------------------------------------------------------------
# Imports
# ---------------------------------------------------------------------------

# Built-in stopwatch module.
import time

# Reads the .env file so TYPESAFE_API_KEY is available.
from dotenv import load_dotenv

# Choice         -> Jev picks ONE option from a list
# TypeSafeClient -> talks to the TypeSafe AI servers
from typesafe_sdk import Choice, TypeSafeClient

# ---------------------------------------------------------------------------
# Setup
# ---------------------------------------------------------------------------

# Load the API key from the .env file.
load_dotenv()  # loads TYPESAFE_API_KEY from the .env file

# Create the client (it picks up TYPESAFE_API_KEY automatically).
client = TypeSafeClient()  # reads TYPESAFE_API_KEY automatically

# ---------------------------------------------------------------------------
# The question: defined ONCE here and reused for every message below
# ---------------------------------------------------------------------------

# We keep the question in a variable so we don't have to repeat it inside the loop.
questions = {
    # "team" is the name we'll use to read the answer later.
    "team": Choice(
        # What we want Jev to decide.
        instructions="Which team should handle this",
        # The three possible answers, each with a short description to guide Jev.
        # Note: the options are in English, but the messages below are not.
        # Jev still matches them correctly.
        criteria={
            "payments": "Money, fees or refund issues",
            "tech": "Login, app or video problems",
            "courses": "Questions about course content",
        },
    ),
}

# ---------------------------------------------------------------------------
# The test messages: a list of (label, text) pairs
# ---------------------------------------------------------------------------

# Each item is a "tuple" of two values: a label to print, and the message to send.
messages = [
    # Plain English.
    ("English", "I paid twice for the course. Please help."),
    # Tanglish = Tamil words typed with English letters (very common in chats and SMS).
    ("Tanglish", "Course ku rendu thadava pay panniten, help pannunga."),
    # The same sentence written in Tamil script.
    ("Tamil", "கோர்ஸுக்கு ரெண்டு தடவை பணம் கட்டிட்டேன். உதவி பண்ணுங்க."),
    # A vague message with no clear topic. We expect LOW confidence here.
    ("Vague", "Ok sir, will see and tell."),
]

# ---------------------------------------------------------------------------
# Send each message to Jev and print the result on one line
# ---------------------------------------------------------------------------

# Blank line before the results.
print()

# Loop over the list. On each pass, "label" gets the first value and "text" the second.
for label, text in messages:
    # Start the stopwatch for this message.
    start = time.perf_counter()
    # Ask Jev, then go straight to the "team" answer:
    #   client.system_one(...)  -> sends the request and returns the full response
    #   .answers["team"]        -> picks out the answer to our "team" question
    team = client.system_one(state=text, questions=questions).answers["team"]
    # Stop the stopwatch and convert to milliseconds.
    ms = (time.perf_counter() - start) * 1000
    # Print one tidy row. The format codes line up the columns:
    #   {label:9}            -> label padded to 9 characters wide
    #   {team.choice:9}      -> chosen team padded to 9 characters wide
    #   {team.confidence:5.0%} -> confidence as a percentage, 5 characters wide
    #   {ms:4.0f}            -> milliseconds as a whole number, 4 characters wide
    print(f"{label:9} -> {team.choice:9} {team.confidence:5.0%} sure   {ms:4.0f} ms")

# Final blank line.
print()
