# Word Practice App (MVP) — GitHub Models (Azure OpenAI o4-mini)

A terminal-based vocabulary practice app (flashcards-style) with an LLM-powered “teacher”.
This project uses **GitHub Models** with the **Azure OpenAI o4-mini** model.

## Features (MVP)
- TUI practice loop (one word at a time)
- Free-form answers
- Semantic evaluation via LLM (not strict string match)
- Verdict: correct / partial / incorrect
- Concise feedback + improved answer
- Teacher personas (tone only)
- Graceful AI failure (shows error and continues)

## Setup
1) Create a GitHub token and enable GitHub Models access for your account/org.
2) Copy environment file:
```bash
cp .env.example .env
```
3) Edit `.env` and set `GITHUB_TOKEN`.

## Run
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python main.py
```

## Deck
Edit `data/deck.json` to add your own words and target meanings.
