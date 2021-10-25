import pytest
import client
import sqlite3


def pytest_addoption(parser):
    parser.addoption('--port', action='store')


@pytest.fixture(scope='session')
def port(request):
    return request.config.getoption('--port')


@pytest.fixture(scope='session')
def base_url(port):
    return f'http://localhost:{port}'


@pytest.fixture(scope='session')
def nonexisting_endpoint(base_url):
    return client.APIClient(base_url, 'v1/none')


@pytest.fixture(scope='session')
def objects(base_url):
    return client.APIClient(base_url, 'v1/objects')


@pytest.fixture(scope='class')
def reset_db():
    with sqlite3.connect('model/demo.db') as db:
        cur = db.cursor()
        cur.execute('''DROP TABLE test''')
        cur.execute('''CREATE TABLE test (
    id INTEGER NOT NULL,
    x FLOAT,
    y FLOAT,
    PRIMARY KEY(id)
    );''')
        cur.execute('''INSERT INTO test(x, y) VALUES (1.1, 2.2);''')
        db.commit()
