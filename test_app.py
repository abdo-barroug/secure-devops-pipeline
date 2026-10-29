
import pytest

from app import app, tasks


@pytest.fixture
def client():
    tasks.clear()

    # Remise à zéro du compteur pour rendre les tests reproductibles.
    import app as application
    application.next_task_id = 1

    app.config["TESTING"] = True

    with app.test_client() as test_client:
        yield test_client


def test_home(client):
    response = client.get("/")

    assert response.status_code == 200
    assert response.json["status"] == "running"


def test_health(client):
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json == {"status": "healthy"}


def test_get_tasks_initially_empty(client):
    response = client.get("/tasks")

    assert response.status_code == 200
    assert response.json == []


def test_create_task(client):
    response = client.post(
        "/tasks",
        json={"title": "Learn Docker"}
    )

    assert response.status_code == 201
    assert response.json["title"] == "Learn Docker"
    assert response.json["completed"] is False


def test_reject_empty_title(client):
    response = client.post(
        "/tasks",
        json={"title": "   "}
    )

    assert response.status_code == 400
    assert "error" in response.json


def test_reject_invalid_json_body(client):
    response = client.post("/tasks", json=["not", "an", "object"])

    assert response.status_code == 400
    assert "error" in response.json
