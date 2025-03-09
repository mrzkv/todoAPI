import httpx
import pytest
from src.services.config import IP_ADDRESS, SERVER_PORT
import random
import string

BASE_URL = f"http://{IP_ADDRESS}:{SERVER_PORT}/v1/api"


def generate_random_name(length=8):
    return "user_" + "".join(random.choices(string.ascii_lowercase, k=length))


def generate_valid_password():
    return (
        random.choice(string.ascii_uppercase) +
        random.choice(string.ascii_lowercase) +
        random.choice(string.digits) +
        random.choice("@#$%&*") +
        "".join(random.choices(string.ascii_letters + string.digits, k=8))
    )


@pytest.fixture
def test_client():
    return httpx.Client(base_url=BASE_URL, follow_redirects=True)


test_user = {"login": generate_random_name(), "password": generate_valid_password()}


@pytest.fixture
def auth_token(test_client):
    test_client.post("/auth/sign-up", json=test_user)
    response = test_client.post("/auth/sign-in", json=test_user)
    assert response.status_code == 200
    return response.cookies.get("token")


def test_sign_up(test_client):
    response = test_client.post("/auth/sign-up", json=test_user)
    assert response.status_code in [201, 409]


def test_sign_in(test_client):
    response = test_client.post("/auth/sign-in", json=test_user)
    assert response.status_code == 200
    assert "access_token" in response.json()


def test_task_list_unauthorized(test_client):
    response = test_client.get("/tasks/list")
    assert response.status_code == 400


def test_task_list(test_client, auth_token):
    cookies = {"token": auth_token}
    response = test_client.get("/tasks/list", cookies=cookies)
    assert response.status_code == 200
    assert "tasks" in response.json()


def test_create_task(test_client, auth_token):
    cookies = {"token": auth_token}
    task_data = {"name": "Test Task"}
    response = test_client.post("/tasks/create", json=task_data, cookies=cookies)
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_change_task_mode(test_client, auth_token):
    cookies = {"token": auth_token}
    task_data = {"name": "Task to Update"}
    create_response = test_client.post("/tasks/create", json=task_data, cookies=cookies)
    assert create_response.status_code == 200

    task_id = 1
    update_data = {"taskid": task_id, "mode": "completed"}
    update_response = test_client.patch("/tasks/change-mode", json=update_data, cookies=cookies)
    assert update_response.status_code == 200
    assert update_response.json()["status"] == "ok"


def test_ping(test_client):
    response = test_client.get("/ping")
    assert response.status_code == 200
    assert "uptime" in response.json()
