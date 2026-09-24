# Jev by TypeSafe AI: Demos

Small Python demos of **Jev**, the System One model from [TypeSafe AI](https://typesafe.ai).
You give Jev plain text plus a few typed questions. It sends back structured answers,
and each answer comes with a probability. Your code then makes the decision.

The running example is a customer-support message that needs to go to the right team.

## What each demo does

### `demo1.py`: Which team gets this message?
The simplest case. It sends a single customer message ("I paid twice for the course...")
to Jev and asks one `Choice` question: should **payments**, **tech** or **courses** handle it?
It prints the team Jev picked, how confident Jev is, and how long the call took.
To see a different result, switch to the commented-out message ("I cannot log in to the app.").

### `demo2.py`: Three questions in one call, plus a traffic light
One call to Jev answers three questions together:
- **team**: a `Choice` between payments, tech and courses
- **frustrated**: a `Noul` (a yes/no probability between 0 and 1) for whether the customer sounds upset
- **urgent**: a `Noul` for whether the message needs action today

It prints every answer, the probability of each team option, and the total time.
Then it turns Jev's confidence into a decision:
- **GREEN** (90% or higher): route automatically
- **YELLOW** (60% to 90%): route it, but flag it for a human to check
- **RED** (below 60%): send it to a human

The point is that Jev supplies the number and your code sets the rule.

### `demo3_tamil.py`: One complaint in several languages
The "I paid twice" complaint goes in as **English**, **Tanglish** (Tamil written in Latin
letters) and **Tamil script**, along with one vague message ("Ok sir, will see and tell.").
The first three should all go to payments with high confidence. The vague message should
come back with low confidence, which is how you know to hand it to a person.

> Windows tip: if Tamil text shows up as boxes, run `chcp 65001` first or use the VS Code terminal.

## Setup

### 1. Get a TypeSafe AI API key
Sign up at [typesafe.ai](https://typesafe.ai) and create an API key.
The docs are at [docs.typesafe.ai](https://docs.typesafe.ai).

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Create your `.env` file
Copy the example file to `.env`:

```bash
# macOS / Linux / Git Bash
cp .env.example .env

# Windows PowerShell
Copy-Item .env.example .env
```

Open `.env` and swap the placeholder for your real key:

```
TYPESAFE_API_KEY=your-real-key
```

Each demo calls `load_dotenv()`, which reads the key from `.env`.

### 4. Run a demo
```bash
python demo1.py
python demo2.py
python demo3_tamil.py
```

## ⚠️ Never commit your API key

- **Only put your real key in `.env`.** That file is listed in `.gitignore`, so git won't track it.
- **Keep `.env.example` as a placeholder.** It *is* committed to the repo. If you edit it,
  make sure no real key is in it before you commit.
- Before you push, run `git status` and confirm `.env` is **not** in the list.
- If a key does get pushed to GitHub, **revoke it in your TypeSafe account right away**
  and create a new one. Deleting the commit is not enough, because the key is already public.
