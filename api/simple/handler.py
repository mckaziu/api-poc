from http.server import SimpleHTTPRequestHandler
import json
import model.test_data as td
import functools


class MyHandler(SimpleHTTPRequestHandler):
    def __init__(self, session, *args, **keys):
        self.session = session
        self.operations = td.Operations(self.session)
        super().__init__(*args, **keys)

    def _validate(self):
        parsed = self.path.split('/')
        if parsed[1] == 'v1' and parsed[2] == 'objects':
            return True
        else:
            return False

    def _handle_wrong_endpoint(self):
        self.send_response(404)
        self.send_header('Content-type', 'text/json')
        self.end_headers()
        output_data = {
            'status': '404',
            'message': 'Wrong endpoint',
            'path': self.path
        }
        output_json = json.dumps(output_data)
        self.wfile.write(output_json.encode('utf-8'))

    def _extract_payload(self):
        content_length = int(self.headers['Content-Length'])
        if content_length:
            input_json = self.rfile.read(content_length)
            return json.loads(input_json)
        else:
            return None

    def _extract_id(self):
        parsed = self.path.split('/')
        id = parsed[3] if len(parsed) == 4 else None
        return id

    def validate_request(handler):
        @functools.wraps(handler)
        def wrapper(self):
            if not self._validate():
                self._handle_wrong_endpoint()
                return
            return handler(self)
        return wrapper

    def write_response(handler):
        @functools.wraps(handler)
        def wrapper(self):
            output = handler(self)
            self.send_response(200)
            self.send_header('Content-type', 'text/json')
            self.end_headers()
            self.wfile.write(output.encode('utf-8'))
        return wrapper

    def standard_response(method):
        def inner(handler):
            @functools.wraps(handler)
            def wrapper(self):
                handler(self)
                output = {'status': 'OK', 'result': method}
                output_data = json.dumps(output)
                self.send_response(200)
                self.send_header('Content-type', 'text/json')
                self.end_headers()
                self.wfile.write(output_data.encode('utf-8'))
            return wrapper
        return inner

    @validate_request
    @standard_response('POST')
    def do_POST(self):
        payload = self._extract_payload()
        self.operations.create(payload[0], payload[1])

    @validate_request
    @write_response
    def do_GET(self):
        id = self._extract_id()
        result = self.operations.read(id)
        return json.dumps(result)

    @validate_request
    @standard_response('PUT')
    def do_PUT(self):
        id = self._extract_id()
        input_data = self._extract_payload()
        self.operations.update(id, input_data[0], input_data[1])

    @validate_request
    @standard_response('DELETE')
    def do_DELETE(self):
        id = self._extract_id()
        self.operations.delete(id)
