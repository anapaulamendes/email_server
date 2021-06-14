import datetime
import json
import uuid


def get_request(self):
    length = int(self.headers.get("content-length"))
    request = json.loads(self.rfile.read(length))
    return request


def response(self, json_output):
    return self.wfile.write(json.dumps(json_output).encode("utf-8"))


class Methods:
    def save_user(self):
        request = get_request(self)
        with open("db/users.json", "r+") as file:
            # data = {"users": []}
            data = json.load(file)
            if request["user"] not in data["users"]:
                data["users"].append(request["user"])
                file.seek(0)
                json.dump(data, file)
                return response(self, {"success": True, "response": request})
            else:
                return response(self, {"success": False, "error": "Usuario ja existe"})

    def get_user(self, query_params):
        if query_params is not None:
            user = query_params.split("=")[1]
        with open("db/users.json", "r") as file:
            data = json.load(file)
        if user in data["users"]:
            return response(self, {"success": True, "response": {"user": user}})
        else:
            return response(self, {"success": False, "error": "Usuario nao encontrado"})

    def send_mail(self):
        request = get_request(self)
        email = {"id": str(uuid.uuid4()), "forwarded_to": [], "replies": []}
        email.update(request)
        with open("db/emails.json", "r+") as file:
            # data = []
            data = json.load(file)
            data.append(email)
            file.seek(0)
            json.dump(data, file)
            return response(self, {"success": True, "response": email})

    def list_mails(self, query_params):
        received = []
        sent = []
        if query_params is not None:
            user = query_params.split("=")[1]
        with open("db/emails.json", "r") as file:
            data = json.load(file)
        for email in data:
            if email["receiver"] == user or user in email["forwarded_to"]:
                received.append(email)
            elif email["sender"] == user:
                sent.append(email)
        return response(
            self, {"success": True, "response": {"received": received, "sent": sent}}
        )

    def open_mail(self, query_params):
        if query_params is not None:
            id = query_params.split("=")[1]
        with open("db/emails.json", "r") as file:
            data = json.load(file)
        for email in data:
            if email["id"] == id:
                return response(self, {"success": True, "response": email})

    def replay_mail(self):
        request = get_request(self)
        reply = {
            "datetime": datetime.datetime.now().strftime("%c"),
            "replied_by": request["replied_by"],
            "reply": request["reply"],
        }
        with open("db/emails.json", "r+") as file:
            data = json.load(file)
            for email in data:
                if email["id"] == request["id"]:
                    email["replies"].append(reply)
                    file.seek(0)
                    json.dump(data, file)
                    return response(self, {"success": True, "response": email})

    def forward_mail(self):
        request = get_request(self)
        with open("db/emails.json", "r+") as file:
            data = json.load(file)
            for email in data:
                if email["id"] == request["id"]:
                    email["forwarded_to"].append(request["forward_to"])
                    file.seek(0)
                    json.dump(data, file)
                    return response(self, {"success": True, "response": email})

    def delete_mail(self, query_params):
        if query_params is not None:
            id = query_params.split("=")[1]
        with open("db/emails.json", "r+") as file:
            data = json.load(file)
            for i in range(len(data)):
                if data[i]["id"] == id:
                    del data[i]
                    file.seek(0)
                    json.dump(data, file)
                    return response(
                        self, {"success": True, "response": "E-mail deletado."}
                    )
