# Overview

A sample Python project with examples of APIs in a couple of different styles: pure Python, two types of Flask APIs, FastAPI.

Additionally, project includes a small test suite written in Pytest.

# Usage

1. Run the server using `run_server.py`, e.g.:

`python run_server.py --api=fastapi-restful --port=8000`

The `api` parameter accepts one of the following values: `simple`, `flask-plain`,`flask-restful`, `fastapi`

2. Run tests. Enter `tests` directory, run `pytest --port=PORT` where `PORT` is the port used by the server.

**Note**

Currently the database is not recreated between test runs + the tests assume that `demo.db` has at least one row.

Until this is fixed, please do manual inserts between test runs if you need to re-populate the db, e.g.

`INSERT INTO "main"."test"("ID","X","Y") VALUES (1,1.1,2.2);`

# Contents

## API

- `simple` - Pure Python API implemented using TCPServer and SimpleHTTPRequestHandler
- `flask_plain` - Pure Flask API - uses only routing
- `flask_restful` - Restful Flask API
- `fastapi` - FastAPI example running on Uvicorn

Each of the modules implements `run` function with `port` parameter so that it is easy to select and run the server/API from the `run_server` script.

## Model

- Sample Sqlite database `demo.db` with one table `test`
- Two helper classes using SQLAlchemy's ORM for representing the data and doing CRUD operations on the database

## Tests

- `conftest.py` - fixtures: reading the port from the command line, creating client objects 
- `helpers.py` - a single client class, `APIHelper`, that can send HTTP requests to API to which it is attached
- `test_simple.py` - a single test class for testing the APIs; the test cases cover all of the basic functionality provided by the sample APIs

## `run_server.py`

Script for selecting and running one of the implemented servers/APIs.

# Todo

- reset the db before tests
- more refactoring
- renaming modules and classes where needed
- possibility to run tests on mocked db
- additional endpoint with fancy calculations
- tests for the additional endpoint
- simple performance tests
- finish linting