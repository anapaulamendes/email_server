from datetime import datetime
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, HTTPServer

import methods

PORT = 8000
_methods = methods.Methods


def get_path_and_query_params(self, url):
    if url.find("?") != -1:
        return self.path.split("?")[0], self.path.split("?")[1]
    else:
        return None


class _RequestHandler(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(HTTPStatus.OK)
        self.send_header("Content-type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()

    def do_GET(self):
        self._set_headers()
        self.path, query_params = get_path_and_query_params(self, self.path)

        if self.path == "/":
            _methods.get_user(self, query_params)
        elif self.path == "/listmails":
            _methods.list_mails(self, query_params)
        elif self.path == "/openmail":
            _methods.open_mail(self, query_params)

    def do_POST(self):
        self._set_headers()
        if self.path == "/":
            _methods.save_user(self)
        elif self.path == "/sendmail":
            _methods.send_mail(self)

    def do_PUT(self):
        self._set_headers()
        if self.path == "/replymail":
            _methods.replay_mail(self)
        elif self.path == "/forwardmail":
            _methods.forward_mail(self)

    def do_DELETE(self):
        self._set_headers()
        self.path, query_params = get_path_and_query_params(self, self.path)
        
        if self.path == "/deletemail":
            _methods.delete_mail(self, query_params)

    def do_OPTIONS(self):
        self.send_response(HTTPStatus.NO_CONTENT)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE")
        self.send_header("Access-Control-Allow-Headers", "content-type")
        self.end_headers()


def runserver():
    server_address = ("", PORT)
    http_server = HTTPServer(server_address, _RequestHandler)
    print("Serving at port", PORT)
    http_server.serve_forever()


if __name__ == "__main__":
    runserver()
