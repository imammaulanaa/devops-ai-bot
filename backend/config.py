import os


class Settings:
    APP_NAME: str = "DevOps AI Bot"

    # AI Provider
    AI_PROVIDER: str = os.getenv("AI_PROVIDER", "openai")
    AI_FALLBACK: bool = os.getenv("AI_FALLBACK", "false").lower() == "true"

    # API Keys
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    BLUESMIND_API_KEY: str = os.getenv("BLUESMIND_API_KEY", "")

    # GitHub
    GITHUB_TOKEN: str = os.getenv("GITHUB_TOKEN", "")
    GITHUB_OWNER: str = os.getenv("GITHUB_OWNER", "")

    # Branch
    BASE_BRANCH: str = os.getenv("BASE_BRANCH", "main")


settings = Settings()
