import pytest

from app.config import (
    DEFAULT_INGEST_SECRET,
    DEFAULT_JWT_SECRET,
    Settings,
    check_production_secrets,
)


def _settings(**overrides) -> Settings:
    values = {
        "frontend_url": "http://localhost:3000",
        "jwt_secret": DEFAULT_JWT_SECRET,
        "ingest_secret": DEFAULT_INGEST_SECRET,
    }
    values.update(overrides)
    return Settings(_env_file=None, **values)


def test_local_defaults_are_allowed():
    check_production_secrets(_settings())


def test_deployment_with_default_jwt_secret_fails_fast():
    settings = _settings(
        frontend_url="https://job-board.vercel.app",
        ingest_secret="a-real-ingest-secret",
    )
    with pytest.raises(RuntimeError) as excinfo:
        check_production_secrets(settings)
    assert "JWT_SECRET" in str(excinfo.value)


def test_deployment_with_default_ingest_secret_fails_fast():
    settings = _settings(
        frontend_url="https://job-board.vercel.app",
        jwt_secret="a-real-jwt-secret",
    )
    with pytest.raises(RuntimeError) as excinfo:
        check_production_secrets(settings)
    assert "INGEST_SECRET" in str(excinfo.value)


def test_deployment_with_real_secrets_passes():
    check_production_secrets(
        _settings(
            frontend_url="https://job-board.vercel.app",
            jwt_secret="a-real-jwt-secret",
            ingest_secret="a-real-ingest-secret",
        )
    )


def test_is_local_frontend():
    assert _settings(frontend_url="http://localhost:3000").is_local_frontend
    assert _settings(frontend_url="http://127.0.0.1:3000").is_local_frontend
    assert not _settings(
        frontend_url="https://job-board.vercel.app"
    ).is_local_frontend
