#python -m uvicorn server:app --reload

from uuid import uuid4
from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI()

class Task(BaseModel):
    id: str = None #parâmetro opcional, caso não seja passado, assume o valor None
    name: str = None
    isDone: bool = None #se não for passado, deve assumir o valor False

banco: List[Task] = []

@app.get('/')
def home():
    return {"mensagem": "TudoOK!"}

@app.get('/tasks')
def get_tasks():
    return banco

@app.post('/tasks')
def create_task(task: Task):
    if task.name == None:
        return {'mensagem': 'O nome da tarefa é obrigatório'}
    if task.name in [task.name for task in banco]:
        return {'mensagem': f'A Tarefa {task.name} já foi cadastrada.'}
    if task.id == None:
        task.id = str(uuid4()) #gera um id único se este for None ou se 
    if task.isDone == None:
        task.isDone = False 
    banco.append(task)
    return {'mensagem': f'Tarefa {task.name} de id {task.id} cadastrada com sucesso!'}

@app.get('/tasks/{taskId}')
def get_task(taskId: str):
    for task in banco:
        if task.id == taskId:
            return task
    return {'mensagem': 'Tarefa não encontrada'}

@app.put('/tasks/{taskId}')
def update_task(taskId: str, task_up: Task):
    for i, task in enumerate(banco):
        if task.id == taskId:
            if task_up.name is None:
                task_up.name = task.name
            else:
                if task_up.name in [task.name for task in banco]:
                    return {'mensagem': f'A Tarefa {task_up.name} já foi cadastrada.'}
            if task_up.id is None: #tem como mudar o id? se não, não precisa disso
                task_up.id = task.id
            if task_up.isDone == None:
                task_up.isDone = task.isDone
            banco[i] = task_up
            return {'mensagem': 'Tarefa atualizada com sucesso'}
    return {'mensagem': 'Tarefa não encontrada'}

@app.delete('/tasks/{taskId}')
def delete_task(taskId: str):
    position = None
    for i, task in enumerate(banco):
        if task.id == taskId:
            position = i
            break
    if position is not None:
        banco.pop(position)
        return {'mensagem': 'Tarefa removida com sucesso'}
    return {'mensagem': 'Tarefa não encontrada'}