import pytest
import helpers


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
    return helpers.APIHelper(base_url, 'v1/none')


@pytest.fixture(scope='session')
def objects(base_url):
    return helpers.APIHelper(base_url, 'v1/objects')
