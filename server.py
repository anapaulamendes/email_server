from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, HTTPServer

import methods

PORT = 8000
_methods = methods.Methods


class _RequestHandler(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(HTTPStatus.OK.value)
        self.send_header("Content-type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()

    def do_GET(self):
        if self.path.find("?") != -1:
            path, param = self.path.split("?")[0], self.path.split("?")[1]
            self.path = path
            query_params = param
        else:
            query_params = None
        if self.path == "/":
            _methods.get_user(self, query_params)
        if self.path == "/listmails":
            _methods.list_mails(self, query_params)
        if self.path == "/openmail":
            _methods.open_mail(self, query_params)

    def do_POST(self):
        if self.path == "/":
            _methods.save_user(self)
        if self.path == "/sendmail":
            _methods.send_mail(self)

    def do_PUT(self):
        if self.path == "/replymail":
            _methods.replay_mail(self)
        if self.path == "/forwardmail":
            _methods.forward_mail(self)

    def do_DELETE(self):
        if self.path.find("?") != -1:
            path, param = self.path.split("?")[0], self.path.split("?")[1]
            self.path = path
            query_params = param
        else:
            query_params = None
        if self.path == "/deletemail":
            _methods.delete_mail(self, query_params)


def run_server():
    server_address = ("", PORT)
    httpd = HTTPServer(server_address, _RequestHandler)
    print("serving at port", PORT)
    httpd.serve_forever()


if __name__ == "__main__":
    run_server()
