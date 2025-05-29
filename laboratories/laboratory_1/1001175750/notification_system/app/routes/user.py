from flask import Blueprint, request, jsonify
from app.models.user import User

# Create a Blueprint named "users" to group user-related routes
users_bp = Blueprint("users", __name__) #Se crea un blueprint llamado "users" para agrupar las rutas de usuario.

# In-memory dictionary to store users (key: username, value: User instance
users_db = {}

def require_auth(f): 
    from functools import wraps
    @wraps(f)
    def decorated(*args, **kwargs):
        if not request.headers.get("Authorization"):
            return jsonify({"error": "Authorization header missing"}), 401
        return f(*args, **kwargs)
    return decorated

@users_bp.route('/users', methods=['POST'])
@require_auth
def register_user():
    """
    Register a new user
    ---
    parameters:
      - name: Authorization
        in: header
        required: true
        type: string
      - in: body
        name: body
        required: true
        schema:
          required: [name, preferred_channel, available_channels]
          properties:
            name:
              type: string
              example: Valentina
            preferred_channel:
              type: string
              example: email
            available_channels:
              type: array
              items:
                type: string
              example: ["email", "sms"]
    responses:
      201:
        description: User created
      400:
        description: User already exists
    """
    data = request.get_json()
    name = data["name"]

     # Check if user already exists
    if name in users_db:
        return jsonify({"error": "User already exists"}), 400

    # Create a new User instance with provided data
    user = User(name, data["preferred_channel"], data["available_channels"])

    # Store the user in the in-memory database
    users_db[name] = user

    return jsonify({"message": "User registered"}), 201

@users_bp.route('/users', methods=['GET'])
@require_auth
def list_users():
    """
    Get all users
    ---
    parameters:
      - name: Authorization
        in: header
        required: true
        type: string
    responses:
      200:
        description: List of users
    """

    # Return a list of all users as dictionaries
    return jsonify([vars(u) for u in users_db.values()])
