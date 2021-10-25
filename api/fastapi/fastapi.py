from fastapi import FastAPI
import uvicorn
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import model.test_data as td
from typing import List

app = FastAPI()
engine = create_engine("sqlite:///model/demo.db")
Session = sessionmaker(bind=engine)

@app.get("/v1/objects")
def get_objects():
    session = Session()
    operations = td.TestOperations(session)
    result = operations.read(None)
    return result

@app.get("/v1/objects/{id}")
def get_object_by_id(id : int):
    session = Session()
    operations = td.TestOperations(session)
    result = operations.read(id)
    return result

@app.post('/v1/objects')
def do_post(o : List[float]):
    session = Session()
    operations = td.TestOperations(session)
    operations.create(o[0], o[1])
    output_data = {'status': 'OK', 'result': 'POST'}
    return output_data

@app.put('/v1/objects/{id}')
def do_put(id : int, o : List[float]):
    session = Session()
    operations = td.TestOperations(session)
    operations.update(id, o[0], o[1])
    output_data = {'status': 'OK', 'result': 'PUT'}
    return output_data

@app.delete('/v1/objects/{id}')
def do_delete(id):
    session = Session()
    operations = td.TestOperations(session)
    operations.delete(id)
    output_data = {'status': 'OK', 'result': 'DELETE'}
    return output_data

def run(port):
    uvicorn.run('api.fastapi.fastapi:app', port=port)