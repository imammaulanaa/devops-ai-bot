import base64
import logging

import requests
from fastapi import HTTPException

from backend.config import settings

logger = logging.getLogger(__name__)


def _headers() -> dict:
    return {
        "Authorization": f"token {settings.GITHUB_TOKEN}",
        "Accept": "application/vnd.github+json",
    }


def _base_url(repo: str) -> str:
    return f"https://api.github.com/repos/{settings.GITHUB_OWNER}/{repo}"


def _check_response(res: requests.Response, context: str):
    if res.status_code == 401:
        raise HTTPException(status_code=502, detail="GitHub token invalid or expired.")
    if res.status_code == 404:
        raise HTTPException(status_code=404, detail=f"{context}: resource not found.")
    if res.status_code not in (200, 201, 422):
        raise HTTPException(
            status_code=502,
            detail=f"{context} failed ({res.status_code}): {res.text}",
        )


def _get_base_sha(repo: str) -> str:
    url = f"{_base_url(repo)}/git/ref/heads/{settings.BASE_BRANCH}"
    res = requests.get(url, headers=_headers(), timeout=15)

    if res.status_code == 404:
        raise HTTPException(
            status_code=404,
            detail=f"Repo '{settings.GITHUB_OWNER}/{repo}' or branch '{settings.BASE_BRANCH}' not found.",
        )

    _check_response(res, "Get base SHA")

    data = res.json()
    if "object" not in data or "sha" not in data.get("object", {}):
        raise HTTPException(status_code=502, detail=f"Unexpected GitHub response: {data}")

    return data["object"]["sha"]


def _create_branch(repo: str, branch: str, sha: str):
    url = f"{_base_url(repo)}/git/refs"
    res = requests.post(
        url,
        json={"ref": f"refs/heads/{branch}", "sha": sha},
        headers=_headers(),
        timeout=15,
    )

    # 422 = branch already exists, which is acceptable
    if res.status_code == 422:
        logger.warning("Branch '%s' already exists, continuing.", branch)
        return

    _check_response(res, f"Create branch '{branch}'")
    logger.info("Branch '%s' created.", branch)


def _commit_file(repo: str, branch: str, filename: str, content: str, message: str):
    url = f"{_base_url(repo)}/contents/{filename}"
    encoded = base64.b64encode(content.encode()).decode()

    res = requests.put(
        url,
        json={"message": message, "content": encoded, "branch": branch},
        headers=_headers(),
        timeout=15,
    )
    _check_response(res, f"Commit file '{filename}'")
    logger.info("File '%s' committed to branch '%s'.", filename, branch)


def create_pr(repo: str, branch: str, content: str, message: str, filename: str) -> str:
    logger.info("Creating PR: repo=%s, branch=%s, file=%s", repo, branch, filename)

    sha = _get_base_sha(repo)
    _create_branch(repo, branch, sha)
    _commit_file(repo, branch, filename, content, message)

    url = f"{_base_url(repo)}/pulls"
    res = requests.post(
        url,
        json={"title": message, "head": branch, "base": settings.BASE_BRANCH},
        headers=_headers(),
        timeout=15,
    )
    _check_response(res, "Create PR")

    pr_data = res.json()
    html_url = pr_data.get("html_url")

    if not html_url:
        raise HTTPException(status_code=502, detail=f"PR created but no URL returned: {pr_data}")

    logger.info("PR created: %s", html_url)
    return html_url
