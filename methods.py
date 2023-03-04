from http import HTTPStatus
from http.server import CGIHTTPRequestHandler

from controllers import Controllers

controllers = Controllers


def get_route_and_query_param(url):
    if url.find("?") != -1:
        return url.split("?")[0], url.split("?")[1]
    else:
        return url, None


class RequestHandler(CGIHTTPRequestHandler):
    def do_GET(self):
        self.path, query_param = get_route_and_query_param(self.path)

        if self.path == "/":
            controllers.get_user(self, query_param)
        elif self.path == "/listmails":
            controllers.list_mails(self, query_param)
        elif self.path == "/openmail":
            controllers.open_mail(self, query_param)

    def do_POST(self):
        if self.path == "/":
            controllers.save_user(self)
        elif self.path == "/sendmail":
            controllers.send_mail(self)

    def do_PUT(self):
        if self.path == "/replymail":
            controllers.replay_mail(self)
        elif self.path == "/forwardmail":
            controllers.forward_mail(self)

    def do_DELETE(self):
        self.path, query_param = get_route_and_query_param(self.path)

        if self.path == "/deletemail":
            controllers.delete_mail(self, query_param)

    def do_OPTIONS(self):
        self.send_response(HTTPStatus.NO_CONTENT)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header(
            "Access-Control-Allow-Methods", "GET, POST, PUT, DELETE"
        )
        self.send_header("Access-Control-Allow-Headers", "content-type")
        self.end_headers()
