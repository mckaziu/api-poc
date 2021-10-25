from api.simple import server
from api.flask_plain import flask as flask_plain
from api.flask_restful import flask as flask_restful
from api.fastapi import fastapi
import os
from argparse import ArgumentParser

parser = ArgumentParser()
api_choices = ['simple', 'flask-plain', 'flask-restful', 'fastapi']
api_help = "select version of the server and API"
port_help = "select port on which server should run"
parser.add_argument("--api", dest="api", choices=api_choices, required=True, help=api_help)
parser.add_argument("--port", dest="port", type=int, required=True, help=port_help)

args = parser.parse_args()


def run_simple(port):
    server.run(port)


def run_flask_plain(port):
    os.environ['FLASK_APP'] = "./api/flask-plain/flask.py"
    flask_plain.run(port)


def run_flask_restful(port):
    os.environ['FLASK_APP'] = "./api/flask-restful/flask.py"
    flask_restful.run(port)


def run_fastpi(port):
    fastapi.run(port)


runners = {
    'simple': run_simple,
    'flask-plain': run_flask_plain,
    'flask-restful': run_flask_restful,
    'fastapi': run_fastpi
}

runner = runners[args.api]
runner(args.port)
