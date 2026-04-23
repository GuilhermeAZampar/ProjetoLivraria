#importando as bibliotecas

from fastapi import FastAPI , HTTPException
from pydantic import BaseModel
from typing import Optional

#inicializado api
app =FastAPI()

#criando nossa clase q herda o base model
class Tarefa(BaseModel):
    nome: str
    descricao: str
    concluido: bool = False


#lista de tarefas
tarefas=[]


#rota de add , recebe obj tarejas
#para tarefa se o nome for igual , erro se nao coloca na lista d obj
@app.post("/adicionar")
def adicionar_tarefa(tarefa: Tarefa):
    for t in tarefas:
        if t.nome == tarefa.nome:
            raise HTTPException(status_code=404,detail="Erro tarefa ja existente")
        
    tarefas.append(tarefa)
    return{"message":"Tarefa adicionada com sucesso"}
        

#nao recebe nada , apenas se nao tiver tarefas erro se nao imprime
@app.get("/listar")
def listar_tarefa():
    if not tarefas:
        raise HTTPException(status_code=404,detail="Nao ha tarefas para listar")
    else:
        return{"tarefas":tarefas}

#recebe nome como paremetro e confesso q me buguei um pouco
#para cada tarefa se se o nome recebido for igual marca concluido como true
@app.put("/marcar/{nome}")
def concluido(nome:str):
    for t in tarefas:
        if t.nome == nome:
            t.concluido=True
            return{"message":"Tarefa concluida com sucesso"}
    raise HTTPException(status_code=404,detail="Erro nao achamos a tarefa")


#recebe nome tbm , e para cada tarefa enumerada ,
#se tafera nome for igual ao nome exlcui ela 
@app.delete("/deletar/{nome}")
def deletar_tarefa(nome:str):
    for i , t in enumerate(tarefas):
        if t.nome == nome:
            del tarefas[i]
            return{"message":"Tarefa excluida com sucesso"}
        
    raise HTTPException(status_code=404,detail="Erro tarefa nao encontrada")