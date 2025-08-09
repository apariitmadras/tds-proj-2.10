import os, json, httpx
from pathlib import Path
from .schemas import CodePackage

PROMPT = Path("prompts/codegen.txt").read_text(encoding="utf-8")
BASE = os.getenv("OPENAI_API_BASE", "https://api.openai.com/v1")
MODEL = os.getenv("OPENAI_MODEL_CODEGEN", "gpt-4o-mini")
KEY   = os.getenv("OPENAI_API_KEY_CODEGEN")

def generate_code(ep: dict, timeout: float = None) -> CodePackage:
    assert KEY, "Missing OPENAI_API_KEY_CODEGEN"
    payload = {
        "model": MODEL,
        "messages": [
            {"role":"system","content": PROMPT},
            {"role":"user","content": "EP JSON:\n```json\n"+json.dumps(ep, ensure_ascii=False)+"\n```"}
        ],
        "response_format": {"type": "json_object"}
    }
    with httpx.Client(timeout=timeout or float(os.getenv("CODEGEN_TIMEOUT", "40.0"))) as c:
        r = c.post(f"{BASE}/chat/completions",
                   headers={"Authorization": f"Bearer {KEY}"},
                   json=payload)
        r.raise_for_status()
        data = r.json()["choices"][0]["message"]["content"]
    return CodePackage.model_validate_json(data)
