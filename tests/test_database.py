import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from main import Base,LivroDB,app
from dotenv import load_dotenv
import os


load_dotenv()

DATABASE_URL_TEST="sqlite:///memory:"
engine=create_engine(DATABASE_URL_TEST,connect_args={"check_same_thread":False})
TestSessionLocal=sessionmaker(bind=engine)
Base.metadata.create_all(bind=engine)
client=TestClient(app)

@pytest.fixture(autouse=True)
def mock_redis(mocker):
    mock_redis_client=mocker.patch("main.redis_client",autospec=True)
    mock_redis_client.get.return_value=None

@pytest.fixture(scope=function)
def db():
    db= TestSessionLocal()
    try:
        yield db
    finally:
        db.close()


def test_get_livro(db,mocker):
    response=client.get("/livros",auth=("admin","admin"))
    assert response.status_code==200

    data=response.json()
    assert len(data["livros"])==10
    assert data ["livros"] [0] ["nome_livro"]=="Metallica"
    assert data ["livros"] [0] ["autor_livro"]=="JH"
    assert data ["livros"] [0] ["ano_livro"]==2025