from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field, PostgresDsn

class Settings(BaseSettings):
    cors_origins: str = Field(..., validation_alias="CORS_ORIGINS")
    database_url: str = Field(..., alias="DATABASE_URL")

    @property
    def origins(self) -> list[str]:
        return [
            origin.strip()
            for origin in self.cors_origins.split(",")
            if origin.strip()
        ]

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",              # 🔑 allow env vars
        populate_by_name=True        # 🔑 allow alias mapping
    )

settings = Settings()
