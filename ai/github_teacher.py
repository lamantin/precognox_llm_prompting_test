import os
import json
import requests
from dotenv import load_dotenv

load_dotenv()



# Base host only (NO path here!)
ENDPOINT = os.getenv("GITHUB_ENDPOINT", "https://models.github.ai").rstrip("/")
MODEL = os.getenv("GITHUB_MODEL", "openai/gpt-4o-mini")
TOKEN = os.getenv("GITHUB_TOKEN")

HEADERS = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json",
    "Accept": "application/vnd.github+json",
    "X-GitHub-Api-Version": "2022-11-28",
}

SYSTEM = (
    "You are a strict but helpful vocabulary teacher. "
    "Grade semantically (meaning-based), allow paraphrases and partial credit. "
    "Persona changes style only, not grading criteria. "
    "Return ONLY valid JSON, no markdown, no extra text."
)

def _extract_json(text: str) -> str:
    start = text.find("{")
    end = text.rfind("}")
    if start == -1 or end == -1 or end <= start:
        raise ValueError(f"Model output did not contain a JSON object. Output was: {text[:200]}")
    return text[start : end + 1]

def evaluate(word: str, target_meaning: str, student_answer: str, persona: str) -> dict:

    #print("ENDPOINT =", ENDPOINT)
    #print("MODEL =", MODEL)
    #print("TOKEN starts =", (TOKEN or "")[:6])
    if not TOKEN:
        raise RuntimeError("Missing GITHUB_TOKEN. Copy .env.example to .env and set your token.")

    user_prompt = f"""Persona: {persona}

word: {word}
target_meaning: {target_meaning}
student_answer: {student_answer}

Rubric:
- correct: captures the core meaning accurately; minor wording issues acceptable
- partial: some correct meaning but missing important qualifiers / too vague / small misconception
- incorrect: substantially wrong or unrelated

Return ONLY this JSON schema:
{{
  "verdict": "correct|partial|incorrect",
  "score": 0-100,
  "feedback": ["1-3 short bullet sentences"],
  "improved_answer": "short clear model answer",
  "key_points_missing": ["missing concepts (can be empty)"],
  "persona_line": "optional brief in-character line (can be empty)"
}}
"""

    payload = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": SYSTEM},
            {"role": "user", "content": user_prompt},
        ],
        "temperature": 0.2,
    }

    url = f"{ENDPOINT}/inference/chat/completions"
    r = requests.post(url, headers=HEADERS, json=payload, timeout=60)

    # Ha hibázik, írd ki a választ is (nagyon hasznos debug)
    if not r.ok:
        raise RuntimeError(f"GitHub Models error {r.status_code}: {r.text}")

    content = r.json()["choices"][0]["message"]["content"]
    json_text = _extract_json(content)
    return json.loads(json_text)
