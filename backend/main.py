import asyncio
import logging

from dotenv import load_dotenv
from fastapi import FastAPI

from backend.models.request import GeneratePRRequest, GeneratePRResponse
from backend.services.ai_service import generate_code
from backend.services.github_service import create_pr

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s - %(message)s",
)

app = FastAPI(
    title="DevOps AI Bot",
    description="AI-powered bot that generates code and creates GitHub Pull Requests.",
    version="1.0.0",
)


@app.get("/", tags=["Health"])
def health():
    return {"status": "ok"}


@app.post("/generate-pr", response_model=GeneratePRResponse, tags=["AI"])
async def generate_pr(req: GeneratePRRequest):
    code = await asyncio.to_thread(generate_code, req.prompt)

    pr_url = await asyncio.to_thread(
        create_pr,
        repo=req.repo,
        branch=req.branch,
        content=code,
        message=req.commit_message,
        filename=req.filename,
    )

    return GeneratePRResponse(
        pr_url=pr_url,
        branch=req.branch,
        message="PR successfully created",
    )
