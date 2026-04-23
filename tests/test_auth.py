from fastapi.testclient import TestClient
from main import app
from dotenv import load_dotenv
import os
import pytest
load_dotenv()


client=TestClient(app)
os.environ["meu_usuario"]=="admin"
os.environ["minha_senha"]=="admin"


@pytest.fixture(autouse=True)
def mocker_redis(mocker):
    mocker_redis_client=mocker.patch("main.redis_client",autospec=True)
    mocker_redis_client.get.return_value=None



def test_autenticacao():
    response=client.get("/livros",auth=("admin","admin"))
    assert response.status_code==200



def test_autenticacao_usuario_com_erro():
    response=client.get("/livros",auth=("usuario_errado","admin"))

    assert response.status_code==401
    assert response.json()["detail"]=="Usario ou senha incorretos"



def test_autenticacao_senha_com_erro():
    response=client.get("/livros",auth=("admin","erro"))

    assert response.status_code==401
    assert response.json()["detail"]=="Usario ou senha incorretos"

