from flask import Flask, request, jsonify
from flasgger import Swagger, swag_from
from app.services import UserService, NotificationService
from app.patterns.logger import AppLogger
from app.errors import register_error_handlers, UserNotFoundError, InvalidUsageError
from app.models import User # For type hinting and potential direct use
from swagger_config import SWAGGER_TEMPLATE, SWAGGER_CONFIG # Or define template directly here

app = Flask(__name__)
Swagger(app, template=SWAGGER_TEMPLATE, config=SWAGGER_CONFIG)
register_error_handlers(app)

user_service = UserService()
notification_service = NotificationService()
logger = AppLogger.get_instance()

@app.route('/users', methods=['POST'])
@swag_from({
    'tags': ['Users'],
    'summary': 'Register a new user',
    'description': 'Registers a user with their name, preferred communication channel, and list of available channels.',
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'name': {'type': 'string', 'example': 'Juan'},
                    'preferred_channel': {'type': 'string', 'example': 'email', 'enum': ['email', 'sms', 'console']},
                    'available_channels': {
                        'type': 'array',
                        'items': {'type': 'string', 'enum': ['email', 'sms', 'console']},
                        'example': ['email', 'sms']
                    }
                },
                'required': ['name', 'preferred_channel', 'available_channels']
            }
        }
    ],
    'responses': {
        201: {
            'description': 'User registered successfully',
            'schema': {
                'type': 'object',
                'properties': {
                    'message': {'type': 'string'},
                    'user': {
                        'type': 'object',
                        'properties': {
                            'name': {'type': 'string'},
                            'preferred_channel': {'type': 'string'},
                            'available_channels': {'type': 'array', 'items': {'type': 'string'}}
                        }
                    }
                }
            }
        },
        400: {'description': 'Invalid input data or user already exists'}
    }
})
def register_user():
    """Registers a new user."""
    data = request.get_json()
    if not data:
        raise InvalidUsageError("Request body must be JSON.")
    
    name = data.get('name')
    preferred_channel = data.get('preferred_channel')
    available_channels = data.get('available_channels')

    if not all([name, preferred_channel, available_channels]):
        raise InvalidUsageError("Missing required fields: name, preferred_channel, available_channels.")
    if not isinstance(available_channels, list):
        raise InvalidUsageError("available_channels must be a list.")

    try:
        user = user_service.register_user(name, preferred_channel, available_channels)
        return jsonify({"message": "User registered successfully", "user": user.to_dict()}), 201
    except (ValueError, InvalidUsageError) as e: # Catch specific errors from service/model
        raise InvalidUsageError(str(e))


@app.route('/users', methods=['GET'])
@swag_from({
    'tags': ['Users'],
    'summary': 'List all registered users',
    'description': 'Retrieves a list of all users currently registered in the system.',
    'responses': {
        200: {
            'description': 'A list of users',
            'schema': {
                'type': 'array',
                'items': {
                    'type': 'object',
                    'properties': {
                        'name': {'type': 'string'},
                        'preferred_channel': {'type': 'string'},
                        'available_channels': {'type': 'array', 'items': {'type': 'string'}}
                    }
                }
            }
        }
    }
})
def get_users():
    """Lists all registered users."""
    users = user_service.get_all_users()
    return jsonify(users), 200

@app.route('/users/<string:user_name>', methods=['GET'])
@swag_from({
    'tags': ['Users'],
    'summary': 'Get a specific user by name',
    'description': 'Retrieves details for a specific user.',
    'parameters': [
        {
            'name': 'user_name',
            'in': 'path',
            'type': 'string',
            'required': True,
            'description': 'The name of the user to retrieve.'
        }
    ],
    'responses': {
        200: {
            'description': 'User details',
            'schema': {
                'type': 'object',
                'properties': {
                    'name': {'type': 'string'},
                    'preferred_channel': {'type': 'string'},
                    'available_channels': {'type': 'array', 'items': {'type': 'string'}}
                }
            }
        },
        404: {'description': 'User not found'}
    }
})
def get_user_by_name(user_name: str):
    """Gets a specific user by name."""
    try:
        user = user_service.get_user_by_name(user_name)
        return jsonify(user.to_dict()), 200
    except UserNotFoundError as e:
        raise e # Re-raise to be caught by error handler

@app.route('/notifications/send', methods=['POST'])
@swag_from({
    'tags': ['Notifications'],
    'summary': 'Send a notification to a user',
    'description': 'Sends a notification to a specified user. The system attempts delivery via the user\'s preferred channel, then fallback channels if necessary.',
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'user_name': {'type': 'string', 'example': 'Juan'},
                    'message': {'type': 'string', 'example': 'Your appointment is tomorrow.'},
                    'priority': {'type': 'string', 'example': 'high', 'enum': ['low', 'medium', 'high']}
                },
                'required': ['user_name', 'message']
            }
        }
    ],
    'responses': {
        200: {
            'description': 'Notification sending process initiated.',
            'schema': {
                'type': 'object',
                'properties': {
                    'user_name': {'type': 'string'},
                    'message_sent': {'type': 'string'},
                    'status': {'type': 'string', 'example': 'DELIVERED or DELIVERY_ATTEMPTED_FAILED_ALL_CHANNELS'}
                }
            }
        },
        400: {'description': 'Invalid input data'},
        404: {'description': 'User not found'}
    }
})
def send_notification_endpoint():
    """Sends a notification to a user."""
    data = request.get_json()
    if not data:
        raise InvalidUsageError("Request body must be JSON.")

    user_name = data.get('user_name')
    message = data.get('message')
    priority = data.get('priority', 'medium') # Default priority

    if not all([user_name, message]):
        raise InvalidUsageError("Missing required fields: user_name, message.")

    try:
        result = notification_service.send_notification(user_name, message, priority)
        return jsonify(result), 200
    except UserNotFoundError as e:
        raise e # Re-raise
    except ValueError as e: # Catch other potential issues like invalid channel during factory creation
        raise InvalidUsageError(str(e))


@app.route('/users/<string:user_name>/notifications', methods=['GET'])
@swag_from({
    'tags': ['Notifications'],
    'summary': 'Get notification history for a user',
    'description': 'Retrieves all logged notification attempts for a specific user.',
    'parameters': [
        {
            'name': 'user_name',
            'in': 'path',
            'type': 'string',
            'required': True,
            'description': 'The name of the user whose notification history is to be retrieved.'
        }
    ],
    'responses': {
        200: {
            'description': 'A list of notification attempts for the user.',
            'schema': {
                'type': 'array',
                'items': {
                    'type': 'object',
                    'properties': {
                        'timestamp': {'type': 'string', 'format': 'date-time'},
                        'user_name': {'type': 'string'},
                        'channel': {'type': 'string'},
                        'message': {'type': 'string'},
                        'priority': {'type': 'string'},
                        'status': {'type': 'string'},
                        'details': {'type': 'string'}
                    }
                }
            }
        },
        404: {'description': 'User not found (or no logs for user, though endpoint checks user existence first)'}
    }
})
def get_user_notifications(user_name: str):
    """Gets notification history for a specific user."""
    # First, check if user exists to give a proper 404 if not
    try:
        user_service.get_user_by_name(user_name) 
    except UserNotFoundError as e:
        raise e
        
    user_logs = logger.get_logs(user_name=user_name)
    return jsonify(user_logs), 200

@app.route('/admin/logs/clear', methods=['DELETE'])
@swag_from({
    'tags': ['Admin'],
    'summary': 'Clear all notification logs',
    'description': 'ADMIN Endpoint: Clears all stored notification logs. Use with caution.',
    'responses': {
        200: {'description': 'Logs cleared successfully.'}
    }
})
def clear_all_logs():
    """Clears all notification logs (for admin/testing)."""
    logger.clear_logs()
    # Also clear users_db for a full reset during testing if desired
    # from app.services import users_db
    # users_db.clear()
    # print("Users DB cleared.")
    return jsonify({"message": "All notification logs cleared."}), 200


if __name__ == '__main__':
    # For development:
    # Ensure users_db is accessible if services are instantiated per request
    # In this setup, user_service and notification_service are instantiated once globally,
    # and users_db is a global dict in services.py, so it persists.
    app.run(debug=True)