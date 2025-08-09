import os, json, httpx
from pathlib import Path

PROMPT = Path("prompts/planner.txt").read_text(encoding="utf-8")
BASE = os.getenv("OPENAI_API_BASE", "https://api.openai.com/v1")
MODEL = os.getenv("OPENAI_MODEL_PLANNER", "gpt-4o-mini")
KEY   = os.getenv("OPENAI_API_KEY_PLANNER")

def plan(user_text: str, timeout: float = None) -> dict:
    assert KEY, "Missing OPENAI_API_KEY_PLANNER"
    payload = {
        "model": MODEL,
        "messages": [
            {"role":"system","content": PROMPT},
            {"role":"user","content": user_text + "\n\nReturn only the EP JSON."}
        ],
        "response_format": {"type": "json_object"}
    }
    with httpx.Client(timeout=timeout or float(os.getenv("PLANNER_TIMEOUT", "20.0"))) as c:
        r = c.post(f"{BASE}/chat/completions",
                   headers={"Authorization": f"Bearer {KEY}"},
                   json=payload)
        r.raise_for_status()
        data = r.json()["choices"][0]["message"]["content"]
    return json.loads(data)
