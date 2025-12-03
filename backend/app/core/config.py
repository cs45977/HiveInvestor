from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    SECRET_KEY: str = "your-secret-key-keep-it-secret"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    FINNHUB_API_KEY: str = "mock-key"

    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()
