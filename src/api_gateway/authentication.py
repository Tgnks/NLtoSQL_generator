from src.config import get_jwt_secret
from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime

auth_bp = Blueprint('auth', __name__)

# In-memory user storage for demonstration purposes
users = {}

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    user = users.get(username)
    if user and check_password_hash(user['password'], password):
        token = jwt.encode({
            'username': username,
            'exp': datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=1)
        }, get_jwt_secret(), algorithm='HS256')
        return jsonify({'token': token}), 200
    return jsonify({'message': 'Invalid credentials'}), 401

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if username in users:
        return jsonify({'message': 'User already exists'}), 400

    users[username] = {
        'username': username,
        'password': generate_password_hash(password)
    }
    return jsonify({'message': 'User registered successfully'}), 201

def token_required(f):
    def decorator(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'message': 'Token is missing!'}), 403
        try:
            data = jwt.decode(token, get_jwt_secret(), algorithms=['HS256'])
            current_user = data['username']
        except jwt.PyJWTError:
            return jsonify({'message': 'Token is invalid or expired!'}), 403
        return f(current_user, *args, **kwargs)
    return decorator