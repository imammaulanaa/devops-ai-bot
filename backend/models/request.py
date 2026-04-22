from pydantic import BaseModel, Field
from typing import Optional


class GeneratePRRequest(BaseModel):
    prompt: str = Field(..., example="Create a FastAPI CRUD API for a User model")
    repo: str = Field(..., example="test")
    branch: Optional[str] = Field(default="ai-generated", example="ai-generated")
    filename: Optional[str] = Field(default="ai_generated.py", example="ai_generated.py")
    commit_message: Optional[str] = Field(
        default="feat: auto generated code by AI",
        example="feat: add user CRUD endpoints"
    )


class GeneratePRResponse(BaseModel):
    pr_url: str
    branch: str
    message: str
