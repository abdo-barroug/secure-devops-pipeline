
import pytest

from app import app


@pytest.fixture
def client():
    app.config["TESTING"] = True

    with app.test_client() as client:
        yield client


def test_home(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json["status"] == "running"


def test_health(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json["status"] == "healthy"


def test_get_tasks_initially_empty(client):
    response = client.get("/tasks")
    assert response.status_code == 200
    assert response.json == []


def test_create_task(client):
    response = client.post("/tasks", json={"title": "Test task"})

    assert response.status_code == 201
    assert response.json["title"] == "Test task"
    assert response.json["completed"] is False


def test_reject_empty_title(client):
    response = client.post("/tasks", json={"title": ""})

    assert response.status_code == 400
    assert response.json["error"] == "A non-empty title is required"


def test_reject_invalid_json_body(client):
    response = client.post("/tasks", data="not json")

    assert response.status_code == 400
    assert response.json["error"] == "A JSON object is required"


def test_reject_missing_title(client):
    response = client.post("/tasks", json={})

    assert response.status_code == 400
    assert response.json["error"] == "A non-empty title is required"


def test_reject_whitespace_title(client):
    response = client.post("/tasks", json={"title": "   "})

    assert response.status_code == 400
    assert response.json["error"] == "A non-empty title is required"


def test_reject_non_string_title(client):
    response = client.post("/tasks", json={"title": 123})

    assert response.status_code == 400
    assert response.json["error"] == "A non-empty title is required"


def test_create_task_trims_title(client):
    response = client.post("/tasks", json={"title": "  My task  "})

    assert response.status_code == 201
    assert response.json["title"] == "My task"
