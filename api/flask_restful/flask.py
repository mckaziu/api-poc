from flask import Flask, request
from flask_restful import Resource, Api
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import model.test_data as td

APP_NAME = 'flask-restful-demo-app'
app = Flask(APP_NAME)
app.config["DEBUG"] = True
api = Api(app)

engine = create_engine("sqlite:///model/demo.db")
Session = sessionmaker(bind=engine)


def get_operations():
    session = Session()
    return td.Operations(session)


# TODO: refactor
class MyObjects(Resource):
    def get(self):
        operations = get_operations()
        result = operations.read(None)
        return result

    def post(self):
        operations = get_operations()
        payload = request.json
        operations.create(payload[0], payload[1])
        output_data = {'status': 'OK', 'result': 'POST'}
        return output_data


class MyObject(Resource):
    def get(self, id):
        operations = get_operations()
        result = operations.read(id)
        return result

    def put(self, id):
        operations = get_operations()
        payload = request.json
        operations.update(id, payload[0], payload[1])
        output_data = {'status': 'OK', 'result': 'PUT'}
        return output_data

    def delete(self, id):
        operations = get_operations()
        operations.delete(id)
        output_data = {'status': 'OK', 'result': 'DELETE'}
        return output_data


api.add_resource(MyObjects, '/v1/objects')
api.add_resource(MyObject, '/v1/objects/<id>')


def run(port):
    with engine.connect():
        app.run(host='0.0.0.0', port=port)
