from flask import Blueprint, request, jsonify
from models.user import User

# Define el blueprint para rutas relacionadas con usuarios
users_bp = Blueprint('users', __name__)
users = []  # Lista en memoria para almacenar usuarios

@users_bp.route('/users', methods=['POST'])
def register_user():
    data = request.json
    required_fields = ['name', 'preferred_channel', 'available_channels']

    # Verifica que los campos requeridos estén presentes
    if not data or not all(field in data for field in required_fields):
        return jsonify({'error': 'Missing required fields'}), 400

    # Verifica si el usuario ya está registrado
    if any(u.name == data['name'] for u in users):
        return jsonify({'message': 'User already exists'}), 200

    # Crea y guarda un nuevo usuario
    user = User(data['name'], data['preferred_channel'], data['available_channels'])
    users.append(user)
    return jsonify({'message': 'User registered successfully'}), 201

@users_bp.route('/users', methods=['GET'])
def get_users():
    # Devuelve la lista de usuarios registrados
    users_list = [u.to_dict() for u in users]
    return jsonify(users_list), 200
