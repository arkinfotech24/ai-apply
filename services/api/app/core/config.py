from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    app_name: str = "AI Apply"
    environment: str = "local"
    log_level: str = "INFO"

    database_url: str
    redis_url: str | None = None

    openai_api_key: str | None = None
    openai_model_text: str = "gpt-4.1-mini"
    openai_timeout_seconds: int = 45

    artifacts_dir: str = "/data/artifacts"

settings = Settings()
