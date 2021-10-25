import socketserver
from api.simple.handler import MyHandler
from sqlalchemy import create_engine
import logging
from sqlalchemy.orm import sessionmaker


def handler_factory(Session):
    def createHandler(*args, **keys):
        return MyHandler(Session(), *args, **keys)
    return createHandler


def run(port):
    try:
        logging.basicConfig(level=logging.INFO)
        engine = create_engine("sqlite:///model/demo.db")
        Session = sessionmaker(bind=engine)
        with engine.connect() as db, socketserver.TCPServer(("", port), handler_factory(Session)) as httpd:
            logging.info(f"Starting server at http://localhost:{port}")
            httpd.serve_forever()
    except KeyboardInterrupt:
        logging.info("Stopping server")
        httpd.server_close()
        db.close()
