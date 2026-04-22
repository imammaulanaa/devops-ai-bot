import logging

from backend.services.llm_adapter import LLMAdapter

logger = logging.getLogger(__name__)

_adapter = LLMAdapter()

SYSTEM_PROMPT = "You are a senior software engineer. Write clean, production-ready code with no extra explanation unless asked."


def generate_code(prompt: str) -> str:
    logger.info("Generating code for prompt: %.80s...", prompt)

    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": prompt},
    ]

    res = _adapter.chat_completion(messages)
    return res["choices"][0]["message"]["content"]
