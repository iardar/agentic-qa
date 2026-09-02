from pathlib import Path

from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    openai_api_key: SecretStr | None = None
    llm_model: str = ""

    app_base_url: str = "http://localhost:3000"

    target_repository: Path = Path(".")
    generated_tests_dir: Path = Path("generated_tests")


settings = Settings()
