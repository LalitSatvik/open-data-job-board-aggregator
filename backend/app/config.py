from pydantic_settings import BaseSettings, SettingsConfigDict

DEFAULT_JWT_SECRET = "dev-secret-change-me"
DEFAULT_INGEST_SECRET = "dev-ingest-secret"
LOCAL_FRONTEND_PREFIXES = ("http://localhost", "http://127.0.0.1")


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")

    database_url: str = "sqlite:///./dev.db"
    google_client_id: str = ""
    google_client_secret: str = ""
    jwt_secret: str = DEFAULT_JWT_SECRET
    ingest_secret: str = DEFAULT_INGEST_SECRET
    frontend_url: str = "http://localhost:3000"

    @property
    def is_local_frontend(self) -> bool:
        """True when the frontend runs on the same machine as the backend."""
        return self.frontend_url.startswith(LOCAL_FRONTEND_PREFIXES)


def check_production_secrets(settings: "Settings") -> None:
    """Refuse to start a non-local deployment that still uses dev defaults.

    A deployment whose FRONTEND_URL points somewhere other than localhost is
    reachable from the internet, so booting it with the checked-in default
    signing key would let anyone mint valid session cookies.
    """
    if settings.is_local_frontend:
        return

    unset = []
    if settings.jwt_secret == DEFAULT_JWT_SECRET:
        unset.append("JWT_SECRET")
    if settings.ingest_secret == DEFAULT_INGEST_SECRET:
        unset.append("INGEST_SECRET")

    if unset:
        raise RuntimeError(
            "Refusing to start: "
            + ", ".join(unset)
            + " still holds its development default while FRONTEND_URL is "
            f"{settings.frontend_url!r}. Set a long random value for each in "
            "the deployment environment."
        )


settings = Settings()
check_production_secrets(settings)
