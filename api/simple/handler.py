from http.server import SimpleHTTPRequestHandler
import json
import model.test_data as td

class MyHandler(SimpleHTTPRequestHandler):
    def __init__(self, session, *args, **keys):
        self.session = session
        self.operations = td.TestOperations(self.session)
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
        output_data = {'status': '404', 'message': 'Wrong endpoint', 'path' : self.path}
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

    # TODO: extract decorator (beginning and end)
    def do_POST(self):
        if not self._validate():
            self._handle_wrong_endpoint()
            return

        payload = self._extract_payload()

        self.operations.create(payload[0], payload[1])
        
        output_data = {'status': 'OK', 'result': 'POST'}
        output_json = json.dumps(output_data)

        self.send_response(200)
        self.send_header('Content-type', 'text/json')
        self.end_headers()
        self.wfile.write(output_json.encode('utf-8'))

    def do_GET(self):
        if not self._validate():
            self._handle_wrong_endpoint()
            return

        id = self._extract_id()

        result = self.operations.read(id)
        output_json = json.dumps(result)

        self.send_response(200)
        self.send_header('Content-type','text/json')
        self.end_headers()
        self.wfile.write(output_json.encode('utf-8'))
        
    def do_PUT(self):
        if not self._validate():
            self._handle_wrong_endpoint()
            return

        id = self._extract_id()

        input_data = self._extract_payload()
        self.operations.update(id, input_data[0], input_data[1])

        output_data = {'status': 'OK', 'result': 'PUT'}
        output_json = json.dumps(output_data)

        self.send_response(200)
        self.send_header('Content-type','text/json')
        self.end_headers()
        self.wfile.write(output_json.encode('utf-8'))
        
    def do_DELETE(self):
        if not self._validate():
            self._handle_wrong_endpoint()
            return

        id = self._extract_id()

        self.operations.delete(id)

        output_data = {'status': 'OK', 'result': 'DELETE'}
        output_json = json.dumps(output_data)

        self.send_response(200)
        self.send_header('Content-type','text/json')
        self.end_headers()
        self.wfile.write(output_json.encode('utf-8'))