from http import HTTPStatus
from uuid import uuid4

from fast_zero.schemas import SubmitUserSchema

new_user = SubmitUserSchema(
    username="New User", email="email@email.com", password="password123"
)


def test_read_users_should_return_200_and_empty_when_no_users_created(client):
    response = client.get("/users")
    response_body = response.json()

    assert response.status_code == HTTPStatus.OK
    assert response_body.get("users") == list()
    assert len(response_body.get("users")) == 0


def test_create_user_should_return_201_and_user_data(client):
    response = client.post("/users", json=new_user.model_dump())
    response_body = response.json()

    assert response.status_code == HTTPStatus.CREATED
    assert response_body.get("username") == new_user.username
    assert response_body.get("email") == new_user.email
    assert response_body.get("password") is None
    assert response_body.get("id") is not None


def test_read_users_should_return_200_and_created_user(client):
    response = client.get("/users")
    response_body = response.json()

    assert response.status_code == HTTPStatus.OK
    assert len(response_body.get("users")) == 1

    response_user = response_body.get("users")[0]
    assert response_user.get("username") == new_user.username
    assert response_user.get("email") == new_user.email
    assert response_user.get("password") is None
    assert response_user.get("id") is not None


def test_read_user_should_return_200_and_created_user(client):
    response = client.post("/users", json=new_user.model_dump())
    response_body = response.json()
    new_user_id = response_body.get("id")

    response = client.get(f"/users/{new_user_id}")
    response_body = response.json()

    assert response.status_code == HTTPStatus.OK

    assert response_body.get("username") == new_user.username
    assert response_body.get("email") == new_user.email
    assert response_body.get("password") is None
    assert response_body.get("id") == new_user_id


def test_read_user_should_return_404_when_id_does_not_exist(client):
    response = client.get(f"/users/{uuid4()}")
    assert response.status_code == HTTPStatus.NOT_FOUND


def test_update_users_should_return_200_and_updated_data(client):
    response = client.get("/users")
    response_body = response.json()
    current_user_data = response_body.get("users")[0]

    new_user_data = {
        "username": "1" + current_user_data.get("username"),
        "email": "1" + current_user_data.get("email"),
        "password": "1password",
    }
    user_id = str(current_user_data.get("id"))

    response = client.put(
        f"/users/{user_id}",
        json=new_user_data,
    )

    assert response.status_code == HTTPStatus.OK
    response_body = response.json()
    assert response_body.get("username") == new_user_data.get("username")
    assert response_body.get("email") == new_user_data.get("email")


def test_update_users_should_return_404_when_id_does_not_exist(client):
    user_data = {
        "username": "aaa",
        "email": "bbb@bbb.com",
        "password": "1password",
    }
    user_id = uuid4()

    response = client.put(
        f"/users/{user_id}",
        json=user_data,
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
