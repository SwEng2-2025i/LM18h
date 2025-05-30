from flask import Blueprint, request, jsonify
from app.models.user import User

user_bp = Blueprint('user_bp', __name__)

users = {}  # almacenamiento en memoria

@user_bp.route("/users", methods=["POST"])
def register_user():
    data = request.json
    if not data:
        return jsonify({"error": "Invalid request"}), 400
    try:
        user = User(
            user_id=data.get('id'),
            name=data['name'],
            preferred_channel=data['preferred_channel'],
            channels=data.get('available_channels', [])
        )
    except KeyError as e:
        return jsonify({"error": f"Missing field: {str(e)}"}), 400

    users[user.id] = user
    return jsonify({"message": "User registered", "user_id": user.id}), 201

@user_bp.route("/users", methods=["GET"])
def list_users():
    user_list = [
        {
            "id": u.id,
            "name": u.name,
            "preferred_channel": u.preferred_channel,
            "channels": u.channels
        } for u in users.values()
    ]
    return jsonify(user_list)
