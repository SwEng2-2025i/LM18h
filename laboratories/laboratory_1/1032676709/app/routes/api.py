from flask import jsonify, request
from app.decorators import require_authorization
from app.models.user_store import users
from app.services.notification_service import build_chain
from app import app

@app.route('/users', methods=['POST'])
@require_authorization
def register_user():
    """
    Register a user
    ---
    parameters:
      - in: body
        name: body
        required: true
        schema:
          id: User
          required:
            - name
            - preferred_channel
            - available_channels
          properties:
            name:
              type: string
            preferred_channel:
              type: string
              enum: [email, sms, console]
            available_channels:
              type: array
              items:
                type: string
                enum: [email, sms, console]
      - name: Authorization
        in: header
        type: string
        required: true
    responses:
      201:
        description: User registered
    """
    data = request.get_json()

    # Valida que el canal preferido esté entre los disponibles
    if data['preferred_channel'] not in data['available_channels']:
        return jsonify({"error": "Preferred channel must be in available channels"}), 400
    
    # Guarda el usuario en el "almacenamiento" en memoria
    users[data['name']] = data
    return jsonify({"message": "User registered"}), 201

@app.route('/users', methods=['GET'])
@require_authorization
def list_users():
    """
    List all users
    ---
    parameters:
      - name: Authorization
        in: header
        type: string
        required: true
    responses:
      200:
        description: List of users
    """
    return jsonify(list(users.values()))

@app.route('/notifications/send', methods=['POST'])
@require_authorization
def send_notification():
    """
    Send a notification
    ---
    parameters:
      - in: body
        name: body
        required: true
        schema:
          id: Notification
          required:
            - user_name
            - message
            - priority
          properties:
            user_name:
              type: string
            message:
              type: string
            priority:
              type: string
              enum: [low, medium, high]
      - name: Authorization
        in: header
        type: string
        required: true
    responses:
      200:
        description: Notification result
    """
    data = request.get_json()
    user = users.get(data['user_name'])

    # Retorna error si el usuario no existe
    if not user:
      return jsonify({"error": "User not found"}), 404

    # Construye la cadena de canales con fallback
    chain = build_chain(user['available_channels'], user['preferred_channel'])

    # Envía el mensaje por la cadena y retorna el estado
    success = chain.send(data['message'])
    return jsonify({"status": "delivered" if success else "failed"})