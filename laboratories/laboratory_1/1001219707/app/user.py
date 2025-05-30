from flask import Blueprint, request, jsonify

# Definimos el blueprint para rutas relacionadas con usuarios
user_bp = Blueprint('users', __name__)

# Diccionario en memoria para almacenar los usuarios registrados
# Estructura: { nombre: { preferred: str, available: list[str] } }
users = {}

@user_bp.route('/users', methods=['POST'])
def register_user():
    """
    Registra un nuevo usuario con nombre, canal preferido y canales disponibles.
    ---
    parameters:
      - name: body
        in: body
        required: true
        schema:
          id: User
          properties:
            name:
              type: string
            preferred_channel:
              type: string
            available_channels:
              type: array
              items:
                type: string
    responses:
      201:
        description: Usuario registrado exitosamente
      400:
        description: Datos incompletos o inválidos
    """
    data = request.json
    name = data.get('name')
    preferred = data.get('preferred_channel')
    available = data.get('available_channels')

    # Validación de campos requeridos
    if not name or not preferred or not available:
        return jsonify({'error': 'Missing required fields'}), 400

    # Registro del usuario
    users[name] = {
        'preferred': preferred,
        'available': available
    }

    return jsonify({"message": f"User {name} registered successfully."}), 201

@user_bp.route('/users', methods=['GET'])
def list_users():
    """
    Devuelve todos los usuarios registrados en memoria.
    ---
    responses:
      200:
        description: Lista de usuarios
    """
    return jsonify(users), 200