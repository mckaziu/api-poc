import random
import pytest
from requests.models import HTTPError


# TODO: add mocks
class TestSimpleAPI(object):
    def test_wrong_endpoint(self, nonexisting_endpoint):
        with pytest.raises(HTTPError):
            nonexisting_endpoint._get()

    def test_get_all(self, objects):
        response = objects._get()
        assert isinstance(response, list)
        assert all(map(lambda o: len(o) == 2, response))

    def test_get_by_id(self, objects):
        response = objects._get()
        o = response[0]
        id = o['id']
        response = objects._get(id)
        assert isinstance(response, list)
        assert len(response) == 1
        o = response[0]
        assert o['id'] == id

    def test_get_by_nonexisting_id(self, objects):
        response = objects._get(9999)
        assert isinstance(response, list)
        assert len(response) == 0

    def test_create(self, objects):
        payload = [random.random(), random.random()]
        objects._post(payload)
        response = objects._get()
        o = response[-1]
        assert o['values'] == payload

    def test_update(self, objects):
        response = objects._get()
        o = response[0]
        id = o['id']
        values = o['values']
        payload = [values[0], values[1]+1]
        objects._put(id, payload)
        response = objects._get(id)
        o = response[0]
        assert o['values'] == payload

    def test_delete(self, objects):
        response = objects._get()
        count = len(response)
        o = response[0]
        id = o['id']
        objects._delete(id)
        response = objects._get()
        assert len(response) == count-1
        response = objects._get(id)
        assert len(response) == 0

    def test_delete_nonexisting(self, objects):
        response = objects._get()
        count = len(response)
        objects._delete(9999)
        response = objects._get()
        assert len(response) == count

    def test_idempotency_get(self, objects):
        response = objects._get()
        o = response[0]
        id = o['id']
        response = objects._get(id)
        response2 = objects._get(id)
        assert response == response2

    def test_idempotency_put(self, objects):
        response = objects._get()
        o = response[0]
        id = o['id']
        values = o['values']
        payload = [values[0], values[1]+1]
        objects._put(id, payload)
        response = objects._get(id)
        objects._put(id, payload)
        response2 = objects._get(id)
        assert response == response2

    def test_idempotency_delete(self, objects):
        response = objects._get()
        count = len(response)
        o = response[0]
        id = o['id']
        objects._delete(id)
        objects._delete(id)
        response = objects._get()
        assert len(response) == count-1
        response = objects._get(id)
        assert len(response) == 0
