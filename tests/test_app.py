from http import HTTPStatus

from fastapi.testclient import TestClient

from fast_zero.app import app


def test_get_root_deve_retornar_200_OK_e_mensagem():
    client = TestClient(app)

    response = client.get("/")

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"message": "Olá, mundo!"}
