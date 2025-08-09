import os, httpx
from pathlib import Path

def scrape_website(url: str, output_file: str, timeout: float = 20.0) -> dict:
    r = httpx.get(url, timeout=timeout, headers={"User-Agent":"Mozilla/5.0"})
    r.raise_for_status()
    out = Path(output_file)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(r.text, encoding="utf-8")
    return {"ok": True, "file": str(out), "url": url}
