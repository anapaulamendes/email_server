# Implementação de um serviço de mensagens - Servidor

## Propósito:

Utilizando WebServices no modelo REST, desenvolva um servidor de e-mail simplificado.
Ele deve implementar, pelo menos, as seguintes funcionalidades:

- Enviar mensagem
- Listar mensagens
- Apagar mensagens
- Abrir mensagem
- Encaminhar mensagem
- Responder Mensagem

Desenvolva também um cliente que utilize o servidor através de chamadas às funcionalidades implementadas.
Ao conectar, o usuário deve informar seu nome. Esta será a forma de identificação.
Não é necessário preocupar-se com autenticação. As mensagens podem ser armazenadas em um simples arquivo texto.
Cada mensagem deve conter, pelo menos, os seguintes campos:

- Remetente
- Destinatário
- Assunto
- Corpo

Observações:

1. As aplicações cliente e servidor devem executar facilmente em um computador, sem a necessidade de instalação
   de grandes pacotes de desenvolvimento. Não serão aceitas aplicações executando na web.

2. Deve ser anexado juntamente com o código, um documento em modo texto(README) contendo as informações
   necessárias para a instalação e testes da aplicação.

3. Utilize os métodos HTTP de acordo com o que é especificado pelo modelo REST.

4. Não devem ser utilizadas frameworks no desenvolvimento do servidor que ocultem detalhes do modelo REST.
   Afinal, a proposta principal é que vocês entendam como esse modelo funciona. Utilize uma biblioteca
   semelhante a apresentada na videoaula(JAX-WS).

5. No desenvolvimento do cliente, podem ser utilizadas quaisquer ferramentas e frameworks disponíveis.


## Especificações e tecnologias utilizadas:

- [Python 3.8.9](https://www.python.org/downloads/release/python-389/)
- [http.server](https://docs.python.org/3/library/http.server.html)
- [JSON](https://www.json.org/json-en.html)
- [Linux KDE neon 5.22](https://kde.org/info/plasma-5.22.0/)

> Operating System: KDE neon 5.22
> 
> KDE Plasma Version: 5.22.0
> 
> KDE Frameworks Version: 5.82.0
> 
> Qt Version: 5.15.3
> 
> Kernel Version: 5.4.0-74-generic (64-bit)
> 
> Graphics Platform: X11
> 
> Processors: 8 × Intel® Core™ i5-8265U CPU @ 1.60GHz
> 
> Memory: 7,6 GiB of RAM
> 
> Graphics Processor: Mesa Intel® UHD Graphics 620


## Rodando o servidor:

```
python3 server.py
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
  "response": "E-mail deletado."
}
```

### Exemplos de logs do servidor

```shell
serving at port 8000
127.0.0.1 - - [13/Jun/2021 22:31:08] "POST / HTTP/1.1" 200 -
127.0.0.1 - - [13/Jun/2021 22:31:20] "POST / HTTP/1.1" 200 -
127.0.0.1 - - [13/Jun/2021 22:31:30] "POST / HTTP/1.1" 200 -
127.0.0.1 - - [13/Jun/2021 22:32:02] "GET /?user=ana HTTP/1.1" 200 -
127.0.0.1 - - [13/Jun/2021 22:32:07] "GET /?user=paula HTTP/1.1" 200 -
127.0.0.1 - - [13/Jun/2021 22:32:10] "GET /?user=maria HTTP/1.1" 200 -
127.0.0.1 - - [13/Jun/2021 22:32:13] "GET /?user=ma HTTP/1.1" 200 -
127.0.0.1 - - [13/Jun/2021 22:32:43] "POST /sendmail HTTP/1.1" 200 -
127.0.0.1 - - [13/Jun/2021 22:33:08] "POST /sendmail HTTP/1.1" 200 -
127.0.0.1 - - [13/Jun/2021 22:33:34] "POST /sendmail HTTP/1.1" 200 -
127.0.0.1 - - [13/Jun/2021 22:34:30] "GET /listmails?user=ana HTTP/1.1" 200 -
127.0.0.1 - - [13/Jun/2021 22:34:37] "GET /listmails?user=paula HTTP/1.1" 200 -
127.0.0.1 - - [13/Jun/2021 22:34:40] "GET /listmails?user=maria HTTP/1.1" 200 -
127.0.0.1 - - [13/Jun/2021 22:35:15] "GET /openmail?id=64f03f26-b4d6-41ad-b236-876b8d53b895 HTTP/1.1" 200 -
127.0.0.1 - - [13/Jun/2021 22:35:41] "GET /openmail?id=67eec8ab-8432-4de1-a7e0-12c5656cd010 HTTP/1.1" 200 -
127.0.0.1 - - [13/Jun/2021 22:35:57] "GET /openmail?id=0a8a747c-a0f4-4510-afb3-14e49531d6f0 HTTP/1.1" 200 -
127.0.0.1 - - [13/Jun/2021 22:36:57] "PUT /replymail HTTP/1.1" 200 -
127.0.0.1 - - [13/Jun/2021 22:37:15] "PUT /replymail HTTP/1.1" 200 -
127.0.0.1 - - [13/Jun/2021 22:37:30] "PUT /replymail HTTP/1.1" 200 -
127.0.0.1 - - [13/Jun/2021 22:38:24] "PUT /forwardmail HTTP/1.1" 200 -
127.0.0.1 - - [13/Jun/2021 22:39:03] "PUT /forwardmail HTTP/1.1" 200 -
127.0.0.1 - - [13/Jun/2021 22:41:05] "DELETE /deletemail?id=67eec8ab-8432-4de1-a7e0-12c5656cd010 HTTP/1.1" 200 -
```
