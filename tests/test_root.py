from http import HTTPStatus


def test_get_root_should_return_200_and_message(client):
    response = client.get("/")

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"message": "Olá, mundo!"}
