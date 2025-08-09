import os, sys, json, time, subprocess
from pathlib import Path
from .schemas import EP, CodePackage
from .tools import scrape_website

def run_code(code: str, timeout_sec: float) -> str:
    tmp = Path("outputs/ep_run.py")
    tmp.write_text(code, encoding="utf-8")
    p = subprocess.run([sys.executable, str(tmp)],
                       capture_output=True, text=True, timeout=timeout_sec)
    if p.returncode != 0 and not p.stdout.strip():
        raise RuntimeError(f"Code failed:\n{p.stderr[:2000]}")
    return p.stdout

def execute(ep_json: dict, cp: CodePackage) -> str:
    ep = EP.model_validate(ep_json)
    # Step 1: scrape
    step1 = [s for s in ep.tool_plan if s["step"] == 1][0]
    scrape_website(**step1["parameters"])
    # Step 2: run code
    return run_code(cp.code, timeout_sec=float(os.getenv("EXECUTION_TIMEOUT", "70")))
