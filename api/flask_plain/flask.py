from flask import Flask, request, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import model.test_data as td

APP_NAME = 'flask-plain-demo-app'
app = Flask(APP_NAME)
app.config["DEBUG"] = True

engine = create_engine("sqlite:///model/demo.db")
Session = sessionmaker(bind=engine)


# TODO: extract decorator
@app.get('/v1/objects')
def do_get_all():
    session = Session()
    operations = td.Operations(session)
    result = operations.read(None)
    return jsonify(result)


@app.get('/v1/objects/<int:object_id>')
def do_get_by_id(object_id):
    session = Session()
    operations = td.Operations(session)
    result = operations.read(object_id)
    return jsonify(result)


@app.post('/v1/objects')
def do_post():
    session = Session()
    operations = td.Operations(session)
    payload = request.json
    operations.create(payload[0], payload[1])
    output_data = {'status': 'OK', 'result': 'POST'}
    return jsonify(output_data)


@app.put('/v1/objects/<int:object_id>')
def do_put(object_id):
    session = Session()
    operations = td.Operations(session)
    payload = request.json
    operations.update(object_id, payload[0], payload[1])
    output_data = {'status': 'OK', 'result': 'PUT'}
    return jsonify(output_data)


@app.delete('/v1/objects/<int:object_id>')
def do_delete(object_id):
    session = Session()
    operations = td.Operations(session)
    operations.delete(object_id)
    output_data = {'status': 'OK', 'result': 'DELETE'}
    return jsonify(output_data)


def run(port):
    with engine.connect():
        app.run(host='0.0.0.0', port=port)
