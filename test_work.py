from flask import Flask, request, jsonify
import jwt
import datetime
from functools import wraps

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'


users = {
    'customer1': 'password1',
    'owner1': 'password2'
}

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')

        if not token:
            return jsonify({'message': 'Token is missing!'}), 401

        try:
            data = jwt.decode(token, app.config['SECRET_KEY'])
        except:
            return jsonify({'message': 'Token is invalid!'}), 401

        return f(*args, **kwargs)

    return decorated

@app.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if username in users:
        return jsonify({'message': 'Username already exists!'}), 400

    users[username] = password

    return jsonify({'message': 'Signup successful!'}), 201

@app.route('/login', methods=['POST'])
def login():
    auth = request.authorization

    if not auth or not auth.username or not auth.password:
        return jsonify({'message': 'Could not verify!'}), 401

    username = auth.username
    password = auth.password

    if username not in users or users[username] != password:
        return jsonify({'message': 'Invalid credentials!'}), 401

    token = jwt.encode({'username': username, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, app.config['SECRET_KEY'])

    return jsonify({'token': token.decode('UTF-8')}), 200

@app.route('/customer', methods=['GET'])
@token_required
def customer():
    return jsonify({'message': 'Welcome, customer!'})

@app.route('/owner', methods=['GET'])
@token_required
def owner():
    return jsonify({'message': 'Welcome, owner!'})

if __name__ == '__main__':
    app.run(debug=True)