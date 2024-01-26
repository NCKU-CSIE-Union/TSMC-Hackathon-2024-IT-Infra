import os
from functools import lru_cache


class Settings:
    github_webhook_secret: str = os.getenv("GITHUB_WEBHOOK_SECRET", None)

    sentry_dsn: str = os.getenv("SENTRY_DSN", None)


@lru_cache()
def get_settings():
    return Settings()
