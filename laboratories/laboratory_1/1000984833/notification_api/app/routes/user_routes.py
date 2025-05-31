# app/routes/user_routes.py

from flask import Blueprint, request, jsonify
from app.services.user_service import add_user, get_all_users

user_bp = Blueprint('user_bp', __name__)

@user_bp.route('/users', methods=['POST'])
def create_user():
    """
    Register a new user.
    ---
    tags:
      - Users
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - name
            - preferred_channel
            - available_channels
          properties:
            name:
              type: string
              example: Juan
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
        description: User created successfully
      400:
        description: Missing fields
    """
    data = request.get_json()
    name = data.get('name')
    preferred_channel = data.get('preferred_channel')
    available_channels = data.get('available_channels')

    if not all([name, preferred_channel, available_channels]):
        return jsonify({"error": "Missing fields"}), 400

    add_user(name, preferred_channel, available_channels)
    return jsonify({"message": f"User {name} created"}), 201


@user_bp.route('/users', methods=['GET'])
def list_users():
    """
    List all registered users.
    ---
    tags:
      - Users
    responses:
      200:
        description: A list of users
        schema:
          type: array
          items:
            type: object
            properties:
              name:
                type: string
                example: Juan
              preferred_channel:
                type: string
                example: email
              available_channels:
                type: array
                items:
                  type: string
                example: ["email", "sms"]
    """
    return jsonify(get_all_users()), 200
