import logging

import requests
from fastapi import HTTPException

from backend.config import settings

logger = logging.getLogger(__name__)


class LLMAdapter:
    def chat_completion(self, messages: list[dict]) -> dict:
        if settings.AI_PROVIDER == "bluesmind":
            try:
                logger.info("Calling Bluesmind...")
                return self._bluesmind_chat(messages)
            except HTTPException as e:
                if settings.AI_FALLBACK:
                    logger.warning(
                        "Bluesmind failed (status=%s: %s). Falling back to OpenAI.",
                        e.status_code,
                        e.detail,
                    )
                    return self._openai_chat(messages)
                raise

        logger.info("Calling OpenAI...")
        return self._openai_chat(messages)

    def _bluesmind_chat(self, messages: list[dict]) -> dict:
        url = "https://api.bluesminds.com/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {settings.BLUESMIND_API_KEY}",
            "Content-Type": "application/json",
        }
        payload = {"model": "gpt-4o-mini", "messages": messages}

        res = requests.post(url, json=payload, headers=headers, timeout=60)

        if res.status_code == 401:
            raise HTTPException(status_code=401, detail="Bluesmind API key invalid or expired.")
        if res.status_code == 402:
            raise HTTPException(status_code=402, detail=f"Bluesmind insufficient credits: {res.text}")
        if res.status_code != 200:
            raise HTTPException(status_code=502, detail=f"Bluesmind error {res.status_code}: {res.text}")

        return self._normalize_response(res.json())

    def _openai_chat(self, messages: list[dict]) -> dict:
        if not settings.OPENAI_API_KEY:
            raise HTTPException(status_code=500, detail="OpenAI API key is not configured.")

        from openai import OpenAI

        client = OpenAI(api_key=settings.OPENAI_API_KEY)
        res = client.chat.completions.create(model="gpt-4.1", messages=messages)

        return {
            "choices": [{"message": {"content": res.choices[0].message.content}}]
        }

    @staticmethod
    def _normalize_response(data: dict) -> dict:
        return {
            "choices": [{"message": {"content": data["choices"][0]["message"]["content"]}}]
        }
