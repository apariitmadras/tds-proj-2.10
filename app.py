import os, uuid, asyncio
from pathlib import Path
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import PlainTextResponse
from pipeline.planner import plan
from pipeline.codegen import generate_code
from pipeline.orchestrator import execute

app = FastAPI(title="Data Analyst Agent (B→C→D)")

@app.post("/api/", response_class=PlainTextResponse)
async def analyze(file: UploadFile = File(...)):
    raw = await file.read()
    user_text = raw.decode("utf-8", errors="replace").strip()
    if not user_text:
        raise HTTPException(400, "Empty input")

    # Budget guard (coarse)
    budget = int(os.getenv("PIPELINE_BUDGET", "160"))

    # B: Planner
    ep = plan(user_text)

    # C: CodeGen
    cp = generate_code(ep)

    # D: Orchestrate (scrape + run)
    out = execute(ep, cp)

    # Return exactly what the program printed
    return out

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=int(os.getenv("PORT", "8000")),
        reload=False
    )
