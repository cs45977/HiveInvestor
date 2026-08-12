from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # No default on purpose: a hardcoded fallback here means anyone who reads
    # this (public) repo can forge a valid JWT for any user if a deploy ever
    # forgets to set SECRET_KEY. Missing env var/.env entry => app refuses to
    # boot instead of silently running with a known-to-the-world secret.
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    FINNHUB_API_KEY: str = "mock-key"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

settings = Settings()
