from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List
import json

class Settings(BaseSettings):
    # App
    environment: str = "development"
    backend_cors_origins: str | List[str] = ["http://localhost:3000"]
    backend_host: str = "0.0.0.0"
    backend_port: int = 8001

    # Database
    database_url: str

    # Redis
    redis_url: str

    # Qdrant
    qdrant_host: str = "qdrant_cineiq"
    qdrant_port: int = 6333

    # MinIO
    minio_endpoint: str
    minio_root_user: str
    minio_root_password: str
    minio_bucket: str = "cineiq-assets"

    # Auth
    clerk_secret_key: str = ""
    next_public_clerk_publishable_key: str = ""

    # External APIs
    tmdb_api_key: str = ""
    groq_api_key: str = ""

    model_config = SettingsConfigDict(
        env_file=".env", 
        env_file_encoding="utf-8", 
        case_sensitive=False,
        extra="ignore"
    )

    @property
    def cors_origins_list(self) -> List[str]:
        if isinstance(self.backend_cors_origins, str):
            try:
                return json.loads(self.backend_cors_origins)
            except json.JSONDecodeError:
                return [origin.strip() for origin in self.backend_cors_origins.split(",") if origin.strip()]
        return self.backend_cors_origins

settings = Settings()
