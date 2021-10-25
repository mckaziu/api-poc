import requests
import json


class APIHelper:
    def __init__(self, base_url, endpoint):
        self.base_url = base_url
        self.endpoint = endpoint
        self.url = self._build_url()

    def _build_url(self):
        return f'{self.base_url}/{self.endpoint}'

    def _post(self, payload):
        response = requests.post(
                url=self.url,
                headers={
                    'Accept': 'application/json',
                    'Content-Type': 'application/json',
                },
                data=json.dumps(payload)
            )
        response.raise_for_status()
        return json.loads(response.text)

    def _get(self, id=None):
        url = f'{self.url}/{id}' if id else self.url
        response = requests.get(
                url=url,
                headers={
                    'Accept': 'application/json',
                    'Content-Type': 'application/json',
                },
            )
        response.raise_for_status()
        return json.loads(response.text)

    def _put(self, id, payload):
        response = requests.put(
                url=f'{self.url}/{id}',
                headers={
                    'Accept': 'application/json',
                    'Content-Type': 'application/json',
                },
                data=json.dumps(payload)
            )
        response.raise_for_status()
        return json.loads(response.text)

    def _delete(self, id):
        response = requests.delete(
                url=f'{self.url}/{id}',
                headers={
                    'Accept': 'application/json',
                    'Content-Type': 'application/json',
                },
            )
        response.raise_for_status()
        return json.loads(response.text)
