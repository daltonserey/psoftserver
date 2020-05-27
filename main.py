import random
import json
import jwt

from flask import Flask
from flask import Response
from flask import request

app = Flask(__name__)

visits = 0
users = {}

@app.route('/api/dados/')
def api_dados():
    global visits
    visits += 1
    authorization = request.headers.get('Authorization')
    if authorization:
        response = Response(json.dumps({
            "visits": visits,
            "dados": [random.randint(0,100) for i in range(10)]
        }), mimetype='text/json')
        response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
        return response

    else:
        response = Response(json.dumps({
            "visits": visits,
            "msg": "sorry, user must be authenticated",
            "error": 401
        }), mimetype='text/json')
        response.status_code = 401
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
