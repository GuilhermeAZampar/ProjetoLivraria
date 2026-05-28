#vamos criar uma api de livros 

#vamos usar get , post, put e delete
#o get busca os dados
#o post adiciona livros
#o put atualiza livros
#o delete deleta

from fastapi import FastAPI , HTTPException,Depends
from fastapi.security import HTTPBasic ,HTTPBasicCredentials
from pydantic import BaseModel
from typing import Optional
from dotenv import load_dotenv
import secrets
import os
import asyncio
import redis
import json
from fastapi import BackgroundTasks
from tasks import somar as task_somar,fatorial as task_fatorial
from celery_app import celery_app
from celery.result import AsyncResult
from kafka_producer import enviar_evento

load_dotenv()

from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker ,Session

import logging.config
import yaml
from elasticsearch import Elasticsearch
from datetime import datetime



DATABASE_URL=os.getenv("DATABASE_URL")
engine= create_engine(DATABASE_URL,connect_args={"check_same_thread":False})
SessionLocal=sessionmaker(autocommit=False,autoflush=False,bind=engine)
Base= declarative_base()

ELASTICSEARCH_URL=os.getenv("ELASTICSEARCH_URL","http://localhost:9200")
ELASTICSEARCH_INDEX=os.getenv("ELASTICSEARCH_INDEX","livros-logs")

REDIS_HOST=os.getenv("REDIS_HOST","localhost")
REDIS_PORT=int(os.getenv("REDIS_PORT","6379"))


redis_client = redis.Redis(
    host=REDIS_HOST,
    port=REDIS_PORT,
    db=0,
    decode_responses=True
)

def get_es():
    return Elasticsearch(
        [ELASTICSEARCH_URL],
        request_timeout=5
    )

with open("logging.yaml") as f:
    config = yaml.safe_load(f)
    logging.config.dictConfig(config)

logger = logging.getLogger("name")
logger.info("API iniciando")

app = FastAPI(
    title = "Api de livros",
    description="Api de livros",
    version ="1.0.0",
    contact={
        "name":"guiga",
        "email":"guiga@gmail.com"

    }
)

meu_usuario = os.getenv("meu_usuario")
minha_senha = os.getenv("minha_senha")
security = HTTPBasic()

meus_livros = {}

class LivroDB(Base):
    __tablename__="Livros"
    id=Column(Integer,primary_key=True,index=True)
    nome_livro = Column(String,index=True)
    autor_livro=Column(String,index=True)
    ano_livro=Column(Integer)


class Livro(BaseModel):
    nome_livro:str
    autor_livro:str
    ano_livro:int

Base.metadata.create_all(bind=engine)

def salvar_redis(id_livro:int,livro:Livro):
    try:
        redis_client.set(f"livro:{id_livro}",json.dumps(livro.model_dump()))
    except:
        pass

def deletar_redis(id_livro:int):
    try:
        redis_client.delete(f"livro:{id_livro}")
    except:
        pass




def sessao_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def autenticar_meu_usuario(credentials:HTTPBasicCredentials = Depends(security)):
    is_user_correct = secrets.compare_digest(credentials.username,meu_usuario)
    is_password_corret= secrets.compare_digest(credentials.password,minha_senha)
    if not(is_user_correct and is_password_corret):
        raise HTTPException(status_code = 401,detail = "Usario ou senha incorretos",headers = {"WWW-Authenticate":"Basic"})
    
    return credentials


@app.post("/calcular/soma")
def somar(a:int,b:int):
    tarefa= task_somar.delay(a,b)
    redis_client.lpush("tarefas_ids",tarefa.id)
    redis_client.ltrim("tarefas_ids",0,49)
    return {"task_id":tarefa.id,"message":"Tarefa enviada para segundo plano"}

@app.post("/calcular/fatorial")
def fatorial(n:int):
    tarefa = task_fatorial.delay(n)
    redis_client.lpush("tarefas_ids",tarefa.id)
    redis_client.ltrim("tarefas_ids",0,49)
    return {"task_id":tarefa.id,"message":"Tarefa enviada para segundo plano"}

@app.get("/tarefas/resultado")
def listar_tarefas():
    ids=redis_client.lrange("tarefas_ids",0,-1)
    tarefa=[]
    for task_id in ids:
        resultado=AsyncResult(task_id,app=celery_app)
        tarefa.append({"tarefas_ids":task_id,"status":resultado.status,"resultado":resultado.result if resultado.successful()else None})
    
    return{"tarefas":tarefa}

@app.get("/debug/redis")
def ver_livros():
    chaves = redis_client.keys("*")
    livros=[]
    for chave in chaves:
        valor = redis_client.get(chave)
        ttl= redis_client.ttl(chave)

        try:
            valor=json.loads(valor)
        except:
            pass

        livros.append({"chave":chave,"valor":valor,"ttl":ttl})
    
    return livros


@app.get("/")
def home():
    logger.info("Alguem acessou o nosso /")
    return{"Hello":"Word"}


async def chamada_externa1():
    await asyncio.sleep(2)
    return "Chamada externa 1"

async def chamada_externa2():
    await asyncio.sleep(2)
    return "Chamada externa 2"

async def chamada_externa3():
    await asyncio.sleep(2)
    return "Chamada externa 3"



@app.get("/chamadas-externa")
async def chamadas():
    tarefa1=asyncio.create_task(chamada_externa1())
    tarefa2=asyncio.create_task(chamada_externa2())
    tarefa3=asyncio.create_task(chamada_externa3())

    resultado1= await tarefa1
    resultado2= await tarefa2
    resultado3=await tarefa3
    return{"mensagem":"Todas as apis foram executadas com sucessso","tarefas":[resultado1,resultado2,resultado3]}


@app.get("/livros")
async def get_livros(
    page:int=1,
    limit:int=10,
    db:Session=Depends(sessao_db),
    credentials:HTTPBasicCredentials=Depends(autenticar_meu_usuario)
):

    if page < 1 or limit < 1:
        raise HTTPException(status_code=400, detail="Erro page ou limit invalidos")

    #cache_key=f"livro:page={page}&limit={limit}"

    #try:
        #cached=redis_client.get(cache_key)

        #if cached:
            #return json.loads(cached)
    #except:
        #pass

    livros = db.query(LivroDB).offset((page-1)*limit).limit(limit).all()

    if not livros:
        response = {"Erro":"esse livro nao existe"}
    else:
        total_livros = db.query(LivroDB).count()

        response = {
            "page": page,
            "limit": limit,
            "total": total_livros,
            "livro": [
                {
                    "id": livro.id,
                    "nome_livro": livro.nome_livro,
                    "autor_livro": livro.autor_livro,
                    "ano_livro": livro.ano_livro
                }
                for livro in livros
            ]
        }

    log = {
        "timestamp": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S"),
        "endpoint": "/livros",
        "usuario": credentials.username,
        "page": page,
        "limit": limit,
        "status": "success" if livros else "not found",
        "total_livros": len(livros)
    }

    logger.info(json.dumps(log))

    try:
        es = get_es()

        if es.ping():

            es.index(
                index=ELASTICSEARCH_INDEX,
                document=log
            )

            print("LOG ENVIADO")

        else:
            print("Elasticsearch nao respondeu")

    except Exception as e:
        print(f"Erro Elasticsearch: {e}")

    #try:
        #redis_client.setex(cache_key,30,json.dumps(response))
    #except:
        #pass

    return response
 

@app.post("/adicionar")
async def post_livro(livro:Livro,db:Session=Depends(sessao_db),credentials:HTTPBasicCredentials=Depends(autenticar_meu_usuario)):
    db_livro = db.query(LivroDB).filter(LivroDB.nome_livro==livro.nome_livro,LivroDB.autor_livro==livro.autor_livro).first()
    if db_livro:
        raise HTTPException(status_code=400,detail="Erro livro ja existente")
    
    novo_livro=LivroDB(nome_livro=livro.nome_livro,autor_livro=livro.autor_livro,ano_livro=livro.ano_livro)
    db.add(novo_livro)
    db.commit()
    db.refresh(novo_livro)

    salvar_redis(novo_livro.id,livro)

    try:
        enviar_evento("livros_eventos",{"acao":"criar","livro":livro.model_dump()})
    except:
        pass

    return{"message":"Livro adicionado com sucesso"}
   

@app.put("/atualizar/{id_livro}")
async def put_livro(id_livro:int,livro:Livro,db:Session=Depends(sessao_db),credentials:HTTPBasicCredentials=Depends(autenticar_meu_usuario)):
    db_livros=db.query(LivroDB).filter(LivroDB.id==id_livro).first()
    if not db_livros:
        raise HTTPException(status_code=404,detail="Erro livro nao encontrado")
    
    db_livros.nome_livro=livro.nome_livro
    db_livros.autor_livro=livro.autor_livro
    db_livros.ano_livro=livro.ano_livro
    
    db.commit()
    db.refresh(db_livros)

    salvar_redis(db_livros.id,livro)

    return{"message":"Livro atualizado com sucesso"}



@app.delete("/deletar/{id_livro}")
async def delete_livro(id_livro : int,db:Session=Depends(sessao_db),credentials:HTTPBasicCredentials=Depends(autenticar_meu_usuario)):
    db_livro = db.query(LivroDB).filter(LivroDB.id==id_livro).first()
    if not db_livro:
        raise HTTPException(status_code=404,detail="Erro livro nao existente no banco de dados")
    
    db.delete(db_livro)
    db.commit()

    deletar_redis(id_livro)

    return{"message":"Livro deletado com sucesso"}



if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)