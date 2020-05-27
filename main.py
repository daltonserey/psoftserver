import time
import random
import json
import jwt

from flask import Flask
from flask import Response
from flask import request

SECRET_FOR_JWT = "minha senha secreta"

app = Flask(__name__)

visits = 0
users = {
    "fake": "123"
}
authorized_tokens = {
    "123456": "fake"
}

def check_authentication(request):
    authorization = request.headers.get('Authorization')
    if authorization is None:
        return None

    if ' ' not in authorization:
        return None

    scheme, credentials = authorization.split(" ", 1)
    if scheme != 'Basic':
        return None
 
    if ':' not in credentials:
        return None

    username, password = credentials.split(":", 1)
    if username not in users:
        return None

    if users[username] != password:
        return None

    return username


def is_authorized(request):
    authorization = request.headers.get('Authorization')
    if authorization:
        scheme, token = authorization.split(" ", 1)

    return authorization and token in authorized_tokens


@app.route('/api/login/')
def api_login():
    username = check_authentication(request)
    if username is None:
        response = Response(json.dumps({
            "visits": visits,
            "msg": "sorry, login failed",
            "error": 401
        }), mimetype='text/json')
        response.status_code = 401
        response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
        return response

    # cenário "dia feliz"
    token = jwt.encode({"timestamp": time.time()}, SECRET_FOR_JWT).decode()
    authorized_tokens[token] = username
    response = Response(json.dumps({
        "visits": visits,
        "token": token
    }), mimetype='text/json')
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    return response




@app.route('/api/dados/')
def api_dados():
    global visits
    visits += 1
    if not is_authorized(request):
        response = Response(json.dumps({
            "visits": visits,
            "msg": "sorry, user must be authenticated",
            "error": 401
        }), mimetype='text/json')
        response.status_code = 401
        response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
        return response

    # cenário "dia feliz"
    response = Response(json.dumps({
        "visits": visits,
        "dados": [random.randint(0,100) for i in range(10)]
    }), mimetype='text/json')
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    return response


@app.route('/api/users/')
def api_users():
    global visits
    visits += 1
    response = Response(json.dumps({
        "visits": visits,
        "users": list(users.keys()),
    }), mimetype='text/json')
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    return response


@app.route('/api/signup/', methods=['POST'])
def signup():
    global visits
    visits += 1
    credenciais = json.loads(request.get_data().decode('utf-8'))
    password = credenciais['password']
    username = credenciais['username']
    if username not in users:
        users[username] = password
        return Response(json.dumps({
            "msg": "user created successfully"
        }), mimetype='text/json')
    else:
        response = Response(json.dumps({'msg': 'ops! user already exists'}))
        response.status_code = 400
        return response


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
