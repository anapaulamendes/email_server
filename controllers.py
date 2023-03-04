import datetime
import json
import uuid

from http import HTTPStatus


def get_request(self):
    length = int(self.headers.get("content-length"))
    request = json.loads(self.rfile.read(length))
    return request


def response(self, json_output):
    return self.wfile.write(json.dumps(json_output).encode("utf-8"))


def set_headers(self, status_code):
    self.send_response(status_code)
    self.send_header("Content-type", "application/json")
    self.send_header("Access-Control-Allow-Origin", "*")
    self.end_headers()


class Controllers:
    def save_user(self):
        request = get_request(self)
        with open("data/users.json", "r+") as file:
            # data = {"users": []}
            data = json.load(file)
            if request["user"] not in data["users"]:
                data["users"].append(request["user"])
                file.seek(0)
                json.dump(data, file)
                set_headers(self, HTTPStatus.OK)
                return response(self, {"success": True, "response": request})
            else:
                set_headers(self, HTTPStatus.CONFLICT)
                return response(self, {
                        "success": False, "error": "Usuário já existe"
                })

    def get_user(self, query_param):
        if query_param is not None:
            user = query_param.split("=")[1]
        else:
            set_headers(self, HTTPStatus.BAD_REQUEST)
            return response(self, {"success": False, "error": "Faltando o parâmetro 'user'"})
        with open("data/users.json", "r") as file:
            data = json.load(file)
        if user in data["users"]:
            set_headers(self, HTTPStatus.OK)
            return response(self, {"success": True, "response": {"user": user}})
        else:
            set_headers(self, HTTPStatus.NOT_FOUND)
            return response(self, {"success": False, "error": "Usuário não encontrado"})

    def send_mail(self):
        request = get_request(self)
        # Verify if users exists
        email = {"id": str(uuid.uuid4()), "forwarded_to": [], "replies": []}
        email.update(request)
        with open("data/emails.json", "r+") as file:
            # data = []
            data = json.load(file)
            data.append(email)
            file.seek(0)
            json.dump(data, file)
            set_headers(self, HTTPStatus.OK)
            return response(self, {"success": True, "response": email})

    def list_mails(self, query_param):
        received = []
        sent = []
        if query_param is not None:
            user = query_param.split("=")[1]
        else:
            set_headers(self, HTTPStatus.BAD_REQUEST)
            return response(self, {"success": False, "error": "Faltando o parâmetro 'user'"})
        with open("data/emails.json", "r") as file:
            data = json.load(file)
        for email in data:
            if email["receiver"] == user or user in email["forwarded_to"]:
                received.append(email)
            elif email["sender"] == user:
                sent.append(email)

        set_headers(self, HTTPStatus.OK)

        return response(
            self,
            {"success": True, "response": {"received": received, "sent": sent}}
        )

    def open_mail(self, query_param):
        if query_param is not None:
            id = query_param.split("=")[1]
        else:
            set_headers(self, HTTPStatus.BAD_REQUEST)
            return response(self, {"success": False, "error": "Faltando o parâmetro 'id'"})
        with open("data/emails.json", "r") as file:
            data = json.load(file)
        for email in data:
            if email["id"] == id:
                set_headers(self, HTTPStatus.OK)
                return response(self, {"success": True, "response": email})

    def replay_mail(self):
        request = get_request(self)
        reply = {
            "datetime": datetime.datetime.now().strftime("%c"),
            "replied_by": request["replied_by"],
            "reply": request["reply"],
        }
        with open("data/emails.json", "r+") as file:
            data = json.load(file)
            for email in data:
                if email["id"] == request["id"]:
                    email["replies"].append(reply)
                    file.seek(0)
                    json.dump(data, file)
                    set_headers(self, HTTPStatus.OK)
                    return response(self, {"success": True, "response": email})

    def forward_mail(self):
        request = get_request(self)
        with open("data/emails.json", "r+") as file:
            data = json.load(file)
            for email in data:
                if email["id"] == request["id"]:
                    email["forwarded_to"].append(request["forward_to"])
                    file.seek(0)
                    json.dump(data, file)
                    set_headers(self, HTTPStatus.OK)
                    return response(self, {"success": True, "response": email})

    def delete_mail(self, query_param):
        if query_param is not None:
            id = query_param.split("=")[1]
        with open("data/emails.json", "r+") as file:
            data = json.load(file)
            for i in range(len(data)):
                if data[i]["id"] == id:
                    del data[i]
                    file.seek(0)
                    file.truncate()
                    json.dump(data, file)
                    set_headers(self, HTTPStatus.OK)
                    return response(
                        self, {"success": True, "response": "Mensagem apagada."}
                    )
