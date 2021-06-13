import datetime
import json
import uuid


class Methods:
    def save_user(self):
        length = int(self.headers.get("content-length"))
        request = json.loads(self.rfile.read(length))
        self._set_headers()
        with open("db/users.json", "r+") as file:
            # data = {"users": []}
            data = json.load(file)
            if request["user"] not in data["users"]:
                data["users"].append(request["user"])
                file.seek(0)
                json.dump(data, file)
                self.wfile.write(
                    json.dumps({"success": True, "response": request}).encode("utf-8")
                )
            else:
                self.wfile.write(
                    json.dumps({"success": False, "error": "Usuario ja existe"}).encode(
                        "utf-8"
                    )
                )

    def get_user(self, query_params):
        self._set_headers()
        if query_params is not None:
            user = query_params.split("=")[1]
        with open("db/users.json", "r") as file:
            data = json.load(file)
        if user in data["users"]:
            self.wfile.write(
                json.dumps({"success": True, "response": {"user": user}}).encode(
                    "utf-8"
                )
            )
        else:
            self.wfile.write(
                json.dumps(
                    {"success": False, "error": "Usuario nao encontrado"}
                ).encode("utf-8")
            )

    def send_mail(self):
        length = int(self.headers.get("content-length"))
        request = json.loads(self.rfile.read(length))
        self._set_headers()
        email = {"id": str(uuid.uuid4()), "forwarded_to": [], "replies": []}
        email.update(request)
        with open("db/emails.json", "r+") as file:
            # data = []
            data = json.load(file)
            data.append(email)
            file.seek(0)
            json.dump(data, file)
            self.wfile.write(
                json.dumps({"success": True, "response": email}).encode("utf-8")
            )

    def list_mails(self, query_params):
        self._set_headers()
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
        self.wfile.write(
            json.dumps(
                {"success": True, "response": {"received": received, "sent": sent}}
            ).encode("utf-8")
        )

    def open_mail(self, query_params):
        self._set_headers()
        if query_params is not None:
            id = query_params.split("=")[1]
        with open("db/emails.json", "r") as file:
            data = json.load(file)
        for email in data:
            if email["id"] == id:
                return self.wfile.write(
                    json.dumps({"success": True, "response": email}).encode("utf-8")
                )

    def replay_mail(self):
        length = int(self.headers.get("content-length"))
        request = json.loads(self.rfile.read(length))
        self._set_headers()
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
                    return self.wfile.write(
                        json.dumps({"success": True, "response": email}).encode("utf-8")
                    )

    def forward_mail(self):
        length = int(self.headers.get("content-length"))
        request = json.loads(self.rfile.read(length))
        self._set_headers()
        with open("db/emails.json", "r+") as file:
            data = json.load(file)
            for email in data:
                if email["id"] == request["id"]:
                    email["forwarded_to"].append(request["forward_to"])
                    file.seek(0)
                    json.dump(data, file)
                    return self.wfile.write(
                        json.dumps({"success": True, "response": email}).encode("utf-8")
                    )

    def delete_mail(self, query_params):
        self._set_headers()
        if query_params is not None:
            id = query_params.split("=")[1]
        with open("db/emails.json", "r+") as file:
            data = json.load(file)
            for i in range(len(data)):
                if data[i]["id"] == id:
                    del data[i]
                    file.seek(0)
                    json.dump(data, file)
                    return self.wfile.write(
                        json.dumps(
                            {"success": True, "response": "E-mail deletado."}
                        ).encode("utf-8")
                    )
