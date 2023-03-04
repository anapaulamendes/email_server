from http.server import HTTPServer

from methods import RequestHandler

PORT = 8000


def runserver():
    server_address = ("", PORT)
    http_server = HTTPServer(server_address, RequestHandler)
    print("Servindo na porta:", PORT)
    print("Você pode acessar em: http://localhost:8000/")
    http_server.serve_forever()


if __name__ == "__main__":
    runserver()
