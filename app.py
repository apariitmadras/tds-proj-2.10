import os
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import PlainTextResponse
from pathlib import Path

from pipeline.planner import plan
from pipeline.codegen import generate_code
from pipeline.orchestrator import execute

app = FastAPI(title="Data Analyst Agent (Planner → CodeGen → Executor)")

@app.get("/")
def root():
    return {"ok": True, "message": "POST /api/ with a 'questions.txt' file"}

@app.get("/api/health")
def health():
    return {
        "ok": True,
        "has_planner_key": bool(os.getenv("OPENAI_API_KEY_PLANNER")),
        "has_codegen_key": bool(os.getenv("OPENAI_API_KEY_CODEGEN")),
        "has_orch_key": bool(os.getenv("OPENAI_API_KEY_ORCH")),  # accepted but not required by this MVP
    }

@app.post("/api/", response_class=PlainTextResponse)
async def analyze(file: UploadFile = File(...)):
    raw = await file.read()
    user_text = raw.decode("utf-8", errors="replace").strip()
    if not user_text:
        raise HTTPException(400, "Empty input")

    # Stage B: Planner
    try:
        ep = plan(user_text)
    except Exception as e:
        raise HTTPException(500, f"Planner failed: {e}")

    # Stage C: CodeGen
    try:
        cp = generate_code(ep)
    except Exception as e:
        raise HTTPException(500, f"Code generation failed: {e}")

    # Stage D: Orchestrate (scrape + run)
    try:
        out = execute(ep, cp)
    except Exception as e:
        raise HTTPException(500, f"Execution failed: {e}")

    # Return exactly what the generated script printed
    return out
