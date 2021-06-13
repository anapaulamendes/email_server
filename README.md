- Criar um usuário

`POST /`

`curl --data "{\"user\":\"ana\"}" --header "Content-Type: application/json" http://localhost:8000`

Request:

```json
{
  "user": "ana"
}
```

Response:

```json
{
  "success": true,
  "response": {
    "user": "ana"
  }
}
```

- Obter um usuário

`GET /?user=ana`

`curl http://localhost:8000/?user=ana`

Response:

```json
{
  "success": true,
  "response": {
    "user": "ana"
  }
}
```

- Enviar mensagem

`POST /sendmail`

`curl --data "{\"sender\":\"ana\",\"receiver\":\"paula\",\"subject\":\"teste\",\"body\":\"Teste\"}" --header "Content-Type: application/json" http://localhost:8000/sendmail`

Request:

```json
{
  "sender": "ana",
  "receiver": "paula",
  "subject": "teste",
  "body": "Teste"
}
```

Response:

```json
{
  "success": true,
  "response": {
    "id": "4cac2c15-3028-4ab1-9dd2-571c3aacc611",
    "sender": "ana",
    "receiver": "paula",
    "subject": "teste",
    "body": "Teste",
    "forwarded_to": [],
    "replies": []
  }
}
```

- Listar mensagens

`GET /listmails?user=ana`

`curl http://localhost:8000/listmails?user=ana`

Response:

```json
{
  "success": true,
  "response": {
    "received": [
      {
        "id": "d0a7cae4-9471-4a81-853f-6aff9eb06d03",
        "sender": "paula",
        "receiver": "ana",
        "subject": "teste3",
        "body": "Teste3",
        "forwarded_to": [],
        "replies": []
      }
    ],
    "sent": [
      {
        "id": "4cac2c15-3028-4ab1-9dd2-571c3aacc611",
        "sender": "ana",
        "receiver": "paula",
        "subject": "teste",
        "body": "Teste",
        "forwarded_to": [],
        "replies": []
      },
      {
        "id": "8eb7f3a0-8552-493d-8786-db7514cd3d0c",
        "sender": "ana",
        "receiver": "paula",
        "subject": "teste2",
        "body": "Teste2",
        "forwarded_to": [],
        "replies": []
      }
    ]
  }
}
```

- Abrir mensagem

`GET /openmail?id=8eb7f3a0-8552-493d-8786-db7514cd3d0c`

`curl http://localhost:8000/openmail?id=8eb7f3a0-8552-493d-8786-db7514cd3d0c`

Response:

```json
{
  "success": true,
  "response": {
    "id": "8eb7f3a0-8552-493d-8786-db7514cd3d0c",
    "sender": "ana",
    "receiver": "paula",
    "subject": "teste2",
    "body": "Teste2",
    "forwarded_to": [],
    "replies": []
  }
}
```

- Responder mensagem

`PUT /replymail`

`curl -X PUT --data "{\"id\":\"8eb7f3a0-8552-493d-8786-db7514cd3d0c\",\"replied_by\":\"paula\",\"reply\":\"Resposta\"}" http://localhost:8000/replymail`

Request:

```json
{
  "id": "8eb7f3a0-8552-493d-8786-db7514cd3d0c",
  "replied_by": "paula",
  "reply": "Resposta"
}
```

Response:

```json
{
  "success": true,
  "response": {
    "id": "8eb7f3a0-8552-493d-8786-db7514cd3d0c",
    "sender": "ana",
    "receiver": "paula",
    "subject": "teste2",
    "body": "Teste2",
    "forwarded_to": [],
    "replies": [
      {
        "datetime": "Sun Jun 13 19:20:32 2021",
        "replied_by": "paula",
        "reply": "Resposta"
      },
      {
        "datetime": "Sun Jun 13 19:20:45 2021",
        "replied_by": "ana",
        "reply": "Resposta2"
      },
      {
        "datetime": "Sun Jun 13 19:20:49 2021",
        "replied_by": "paula",
        "reply": "Resposta3"
      }
    ]
  }
}
```

- Encaminhar mensagem

`PUT /forwardmail`

`curl -X PUT --data "{\"id\":\"8eb7f3a0-8552-493d-8786-db7514cd3d0c\",\"forward_to\":\"maria\"}" http://localhost:8000/forwardmail`

Request:

```json
{
  "id": "8eb7f3a0-8552-493d-8786-db7514cd3d0c",
  "forward_to": "maria",
}
```

Response:

```json
{
  "success": true,
  "response": {
    "id": "8eb7f3a0-8552-493d-8786-db7514cd3d0c",
    "sender": "ana",
    "receiver": "paula",
    "subject": "teste2",
    "body": "Teste2",
    "forwarded_to": ["maria"],
    "replies": [
      {
        "datetime": "Sun Jun 13 19:20:32 2021",
        "replied_by": "paula",
        "reply": "Resposta"
      },
      {
        "datetime": "Sun Jun 13 19:20:45 2021",
        "replied_by": "ana",
        "reply": "Resposta2"
      },
      {
        "datetime": "Sun Jun 13 19:20:49 2021",
        "replied_by": "paula",
        "reply": "Resposta3"
      }
    ]
  }
}
```

- Apagar mensagem

`DELETE /deletemail?id=8eb7f3a0-8552-493d-8786-db7514cd3d0c`

`curl -X DELETE http://localhost:8000/deletemail?id=8eb7f3a0-8552-493d-8786-db7514cd3d0c -H "Accept: application/json"`

Response:

```json
{
  "success": true,
  "response": "E-mail deletado."
}
```
