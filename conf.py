from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field

class Settings(BaseSettings):
    cors_origins: str = Field(..., env="CORS_ORIGINS")

    @property
    def origins(self) -> list[str]:
        return [
            origin.strip()
            for origin in self.cors_origins.split(",")
            if origin.strip()
        ]
    
    model_config = SettingsConfigDict(
        env_file=".env",               # local dev only
        env_file_encoding="utf-8",
        case_sensitive=True
    )

settings = Settings()
