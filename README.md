# Implementação de um serviço de mensagens - Servidor

## Requisitos:

- Python 3

## Descrição:

Um servidor de mensagens utilizando o modelo REST com a introdução do protocolo de aplicação HTTP feito com a lib do Python, http.server.

As seguintes funcionalidades implementadas até agora:

- GET
  - Obter usuário
  - Listar mensagens
  - Obter mensagem

- POST
  - Salvar usuário
  - Enviar mensagem

- PUT (internamente é um POST)
  - Responder mensagem
  - Encaminhar mensagem

- DETELE (internamente é um POST)
  - Apagar mensagem


## Rodando o servidor:

```
python server.py --cgi
```

> O servidor irá rodar na porta 8000 por padrão.
> Pode ser acessado em: http://localhost:8000/

## Documentação da API:

- Criar um usuário

`POST /`

```shell
curl --data "{\"user\":\"ana\"}" --header "Content-Type: application/json" http://localhost:8000
```

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

```shell
curl http://localhost:8000/?user=ana
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

- Enviar mensagem

`POST /sendmail`

```shell
curl --data "{\"sender\":\"ana\",\"receiver\":\"paula\",\"subject\":\"teste\",\"body\":\"Teste\"}" --header "Content-Type: application/json" http://localhost:8000/sendmail
```

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

```shell
curl http://localhost:8000/listmails?user=ana
```

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

```shell
curl http://localhost:8000/openmail?id=8eb7f3a0-8552-493d-8786-db7514cd3d0c
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
    "replies": []
  }
}
```

- Responder mensagem

`PUT /replymail`

```shell
curl -X PUT --data "{\"id\":\"8eb7f3a0-8552-493d-8786-db7514cd3d0c\",\"replied_by\":\"paula\",\"reply\":\"Resposta\"}" http://localhost:8000/replymail
```

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

```shell
curl -X PUT --data "{\"id\":\"8eb7f3a0-8552-493d-8786-db7514cd3d0c\",\"forward_to\":\"maria\"}" http://localhost:8000/forwardmail
```

Request:

```json
{
  "id": "8eb7f3a0-8552-493d-8786-db7514cd3d0c",
  "forward_to": "maria"
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

```shell
curl -X DELETE http://localhost:8000/deletemail?id=8eb7f3a0-8552-493d-8786-db7514cd3d0c -H "Accept: application/json"
```

Response:

```json
{
  "success": true,
  "response": "Mensagem apagada."
}
```

### Exemplos de logs do servidor

```shell
Servindo na porta: 8000
Você pode acessar em: http://localhost:8000/
127.0.0.1 - - [04/Mar/2023 10:31:22] "GET / HTTP/1.1" 400 -
127.0.0.1 - - [04/Mar/2023 10:31:28] "POST / HTTP/1.1" 200 -
127.0.0.1 - - [04/Mar/2023 10:31:32] "POST / HTTP/1.1" 200 -
127.0.0.1 - - [04/Mar/2023 10:31:36] "POST / HTTP/1.1" 200 -
127.0.0.1 - - [04/Mar/2023 10:31:37] "POST / HTTP/1.1" 409 -
127.0.0.1 - - [04/Mar/2023 10:31:40] "GET /?user=paula HTTP/1.1" 200 -
127.0.0.1 - - [04/Mar/2023 10:31:44] "POST /sendmail HTTP/1.1" 200 -
127.0.0.1 - - [04/Mar/2023 10:31:55] "GET /listmails?user=ana HTTP/1.1" 200 -
127.0.0.1 - - [04/Mar/2023 10:32:04] "GET /openmail?id=4d74fa9d-8588-4cab-9d03-5b3accc567dd HTTP/1.1" 200 -
127.0.0.1 - - [04/Mar/2023 10:32:22] "PUT /replymail HTTP/1.1" 200 -
127.0.0.1 - - [04/Mar/2023 10:32:34] "PUT /forwardmail HTTP/1.1" 200 -
127.0.0.1 - - [04/Mar/2023 10:32:42] "DELETE /deletemail?id=4d74fa9d-8588-4cab-9d03-5b3accc567dd HTTP/1.1" 200 -
127.0.0.1 - - [04/Mar/2023 10:32:47] "OPTIONS / HTTP/1.1" 204 -
```
