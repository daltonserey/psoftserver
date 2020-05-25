# web app login

Este repositório contém os arquivos de um pequeno app web que
estamos construindo apenas para exemplificar todos os elementos
envolvidos nos processos de criação de usuários e credenciais,
login, logout e acesso a recursos de forma autenticada e
autorizada. O servidor não tem persistência, mas armazena os
dados no próprio processo, permitindo simular todos os processos.

## backend

O _backend_ é implementado em Flask/Python e é implantado no App
Engine (https://psoftserver.nn.r.appspot.com/). No momento, nosso
backend tem apenas 2 rotas / _endpoints_:

1. `GET /api/users` que retorna um objeto contendo os usernames
   de todos os usuários criados e armazenados; a rota é pública,
   logo não é necessário apresentar credenciais para acessá-la;

2. `POST /api/signup` permite que um novo usuário registre novas
   credenciais (_username_ e _passord_); a rota também é pública,
   porque, neste app, qualquer usuário na internet pode criar uma
   conta no app/site;

### como acessar a API via `curl`?

Você pode acessar os _endpoints_ via `curl`. Seguem exemplos

Para acessar a listagem de usuários cadastrados no site:

```
$ curl https://psoftserver.nn.r.appspot.com/api/users/
```

> Importante: a `/` final é necessária.


Para criar um usuário a partir da linha de comando: 

```
$ curl -X POST https://psoftserver.nn.r.appspot.com/api/signup/ -d '{"username":"fulano", "password":"123455"}'
```
