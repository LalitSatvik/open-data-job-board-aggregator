from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")

    database_url: str = "sqlite:///./dev.db"
    google_client_id: str = ""
    google_client_secret: str = ""
    jwt_secret: str = "dev-secret-change-me"
    ingest_secret: str = "dev-ingest-secret"
    frontend_url: str = "http://localhost:3000"


settings = Settings()
