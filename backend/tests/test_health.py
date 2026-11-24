from fastapi.testclient import TestClient

from leascentry.main import app

client = TestClient(app)


def test_health() -> None:
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_ready_returns_503_when_db_unreachable(monkeypatch) -> None:
    monkeypatch.setenv(
        "DATABASE_URL", "postgresql+asyncpg://nobody:nothing@127.0.0.1:1/none"
    )

    with TestClient(app) as client:
        response = client.get("/health/ready")

    assert response.status_code == 503
    assert response.json() == {"status": "not_ready"}
    assert "nobody" not in response.text


def test_ready_returns_200_with_real_db() -> None:
    with TestClient(app) as client:
        response = client.get("/health/ready")

    assert response.status_code == 200
    assert response.json() == {"status": "ready"}
