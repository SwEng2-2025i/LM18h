from flask import Flask, request
from flask_restful import Resource, Api, reqparse, fields, marshal_with, abort
from flasgger import Swagger, swag_from
import random
from datetime import datetime

# Initialize Flask application and extensions
app = Flask(__name__)
api = Api(app)

# Swagger configuration
swagger_config = {
    "headers": [],
    "specs": [
        {
            "endpoint": 'apispec',
            "route": '/apispec.json',
            "rule_filter": lambda rule: True,
            "model_filter": lambda tag: True,
        }
    ],
    "static_url_path": "/flasgger_static",
    "swagger_ui": True,
    "specs_route": "/swagger/"
}

swagger_template = {
    "swagger": "2.0",
    "info": {
        "title": "Notification Delivery API - Chain Of Responsability Pattern",
        "description": "A Flask REST API implementing Chain of Responsibility pattern for notification delivery with complete attempt tracking",
        "contact": {
            "name": "Manuel Castiblanco",
            "email": "mcastiblancoa@unal.edu.co"
        },
        "version": "1.0.0"
    },
    "host": "localhost:5000",
    "basePath": "/",
    "schemes": ["http"],
    "consumes": ["application/json"],
    "produces": ["application/json"]
}

# Initialize Swagger
swagger = Swagger(app, config=swagger_config, template=swagger_template)

# ------------------------
# DATA STRUCTURES
# ------------------------

# In-memory data storage 
users = []  # List to store user objects
notifications = []  # List to store notification objects
notification_history = []  # List to store all notification attempts (successful and failed)

# Global counters for unique IDs
user_id_counter = 1
notification_id_counter = 1
history_id_counter = 1

# Valid communication channels supported by the system
VALID_CHANNELS = {"email", "sms", "whatsapp"}

#------------------------
# REQUEST PARSERS
# ------------------------

# Parser for user creation/update requests
user_args = reqparse.RequestParser()
user_args.add_argument(
    'name', 
    type=str, 
    required=True, 
    help="Name cannot be blank"
)
user_args.add_argument(
    'preferred_channel', 
    type=str, 
    required=True, 
    help="Preferred channel cannot be blank"
)
user_args.add_argument(
    'available_channels', 
    type=list, 
    location='json', 
    required=True, 
    help="Available channels must be a list"
)

# Parser for notification sending requests
notification_args = reqparse.RequestParser()
notification_args.add_argument(
    'user_name', 
    type=str, 
    required=True, 
    help="Name cannot be blank"
)
notification_args.add_argument(
    'message', 
    type=str, 
    required=True, 
    help="Message cannot be blank"
)
notification_args.add_argument(
    'priority', 
    type=str, 
    required=True, 
    help="Priority has to be high, medium or low"
)

# ------------------------
# OUTPUT FIELD DEFINITIONS
# ------------------------

# Output structure for user objects in API responses
userFields = {
    'id': fields.Integer,
    'name': fields.String,
    'preferred_channel': fields.String,
    'available_channels': fields.List(fields.String),
}

# Output structure for notification objects in API responses
notificationFields = {
    'id': fields.Integer,
    'user_name': fields.String,
    'message': fields.String,
    'priority': fields.String,
    'delivered_via': fields.String,
    'timestamp': fields.String,
    'total_attempts': fields.Integer,
    'success': fields.Boolean
}

# Output structure for notification history (individual attempts)
historyFields = {
    'id': fields.Integer,
    'notification_id': fields.Integer,
    'user_name': fields.String,
    'message': fields.String,
    'priority': fields.String,
    'channel': fields.String,
    'success': fields.Boolean,
    'timestamp': fields.String,
    'attempt_number': fields.Integer
}

# ------------------------
# UTILITY FUNCTIONS
# ------------------------

def log_notification_attempt(notification_id, user_name, message, priority, channel, success, attempt_number):
    """
    Log a notification delivery attempt to the history.
    
    Args:
        notification_id (int): ID of the notification being sent
        user_name (str): Name of the target user
        message (str): Message content
        priority (str): Priority level
        channel (str): Channel attempted
        success (bool): Whether the attempt was successful
        attempt_number (int): Attempt number in sequence
    """
    global history_id_counter
    
    history_entry = {
        'id': history_id_counter,
        'notification_id': notification_id,
        'user_name': user_name,
        'message': message,
        'priority': priority,
        'channel': channel,
        'success': success,
        'timestamp': datetime.now().isoformat(),
        'attempt_number': attempt_number
    }
    
    notification_history.append(history_entry)
    history_id_counter += 1
    
    status = "SUCCESS" if success else "FAILED"
    print(f"Logged attempt #{attempt_number}: {channel} - {status}")

# ------------------------
# CHAIN OF RESPONSIBILITY PATTERN IMPLEMENTATION
# ------------------------

class Handler:
    """
    Abstract base class for the Chain of Responsibility pattern.
    
    Each handler in the chain has a reference to the next handler and
    implements the handle method to process requests or pass them along.
    """
    
    def __init__(self, next_handler=None):
        """
        Initialize handler with optional next handler in chain.
        
        Args:
            next_handler (Handler, optional): Next handler in the chain
        """
        self.next = next_handler

    def handle(self, channel, user, message, notification_id, priority, attempt_number):
        """
        Handle a delivery request or pass it to the next handler.
        
        Args:
            channel (str): Communication channel to attempt
            user (dict): User object containing delivery preferences
            message (str): Message content to deliver
            notification_id (int): ID of the notification
            priority (str): Priority level
            attempt_number (int): Current attempt number
            
        Returns:
            str or None: Channel name if delivery successful, None otherwise
        """
        if self.next:
            return self.next.handle(channel, user, message, notification_id, priority, attempt_number)
        return None


class EmailHandler(Handler):
    """
    Concrete handler for email delivery.
    
    Attempts to deliver messages via email with simulated success/failure.
    """
    
    def handle(self, channel, user, message, notification_id, priority, attempt_number):
        """
        Handle email delivery requests.
        
        Args:
            channel (str): Requested delivery channel
            user (dict): Target user information
            message (str): Message to deliver
            notification_id (int): ID of the notification
            priority (str): Priority level
            attempt_number (int): Current attempt number
            
        Returns:
            str or None: 'email' if successful, otherwise passes to next handler
        """
        if channel == 'email':
            # Simulate random delivery success/failure for demonstration
            success = random.choice([True, False])
            
            # Log the attempt
            log_notification_attempt(
                notification_id, user['name'], message, priority, 
                'email', success, attempt_number
            )
            
            if success:
                print(f"Email sent successfully to {user['name']}")
                return 'email'
            else:
                print(f"Email delivery failed for {user['name']}")
        
        # Pass to next handler if this handler can't process the request
        return super().handle(channel, user, message, notification_id, priority, attempt_number)


class SmsHandler(Handler):
    """
    Concrete handler for SMS delivery.
    
    Attempts to deliver messages via SMS with simulated success/failure.
    """
    
    def handle(self, channel, user, message, notification_id, priority, attempt_number):
        """
        Handle SMS delivery requests.
        
        Args:
            channel (str): Requested delivery channel
            user (dict): Target user information
            message (str): Message to deliver
            notification_id (int): ID of the notification
            priority (str): Priority level
            attempt_number (int): Current attempt number
            
        Returns:
            str or None: 'sms' if successful, otherwise passes to next handler
        """
        if channel == 'sms':
            # Simulate random delivery success/failure for demonstration
            success = random.choice([True, False])
            
            # Log the attempt
            log_notification_attempt(
                notification_id, user['name'], message, priority, 
                'sms', success, attempt_number
            )
            
            if success:
                print(f"SMS sent successfully to {user['name']}")
                return 'sms'
            else:
                print(f"SMS delivery failed for {user['name']}")
        
        # Pass to next handler if this handler can't process the request
        return super().handle(channel, user, message, notification_id, priority, attempt_number)


class WhatsAppHandler(Handler):
    """
    Concrete handler for WhatsApp delivery.
    
    Attempts to deliver messages via WhatsApp with simulated success/failure.
    """
    
    def handle(self, channel, user, message, notification_id, priority, attempt_number):
        """
        Handle WhatsApp delivery requests.
        
        Args:
            channel (str): Requested delivery channel
            user (dict): Target user information
            message (str): Message to deliver
            notification_id (int): ID of the notification
            priority (str): Priority level
            attempt_number (int): Current attempt number
            
        Returns:
            str or None: 'whatsapp' if successful, otherwise passes to next handler
        """
        if channel == 'whatsapp':
            # Simulate random delivery success/failure for demonstration
            success = random.choice([True, False])
            
            # Log the attempt
            log_notification_attempt(
                notification_id, user['name'], message, priority, 
                'whatsapp', success, attempt_number
            )
            
            if success:
                print(f"WhatsApp sent successfully to {user['name']}")
                return 'whatsapp'
            else:
                print(f"WhatsApp delivery failed for {user['name']}")
        
        # Pass to next handler if this handler can't process the request
        return super().handle(channel, user, message, notification_id, priority, attempt_number)


# Create the handler chain: Email -> SMS -> WhatsApp
handler_chain = EmailHandler(SmsHandler(WhatsAppHandler()))

# ------------------------
# API RESOURCES
# ------------------------

class Users(Resource):
    """
    Resource for managing users in the notification system.
    
    Handles user creation and retrieval with communication preferences.
    """
    
    @marshal_with(userFields)
    def get(self):
        """
        Retrieve all users from the system.
        ---
        tags:
          - Users
        summary: Get all users
        description: Returns a list of all registered users with their communication preferences
        responses:
          200:
            description: List of users retrieved successfully
        """
        return users

    @marshal_with(userFields)
    def post(self):
        """
        Create a new user in the system.
        ---
        tags:
          - Users
        summary: Create a new user
        description: Creates a new user with communication preferences and validates input data
        parameters:
          - in: body
            name: user
            description: User data
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
                  description: User's full name
                  example: "Jane Smith"
                preferred_channel:
                  type: string
                  description: User's preferred communication channel
                  example: "email"
                  enum: ["email", "sms", "whatsapp"]
                available_channels:
                  type: array
                  items:
                    type: string
                    enum: ["email", "sms", "whatsapp"]
                  description: List of available communication channels
                  example: ["email", "sms", "whatsapp"]
        responses:
          201:
            description: User created successfully
          400:
            description: Invalid input data
        """
        global user_id_counter
        args = user_args.parse_args()

        preferred = args['preferred_channel']
        available = args['available_channels']

        # Validate preferred channel is in allowed channels
        if preferred not in VALID_CHANNELS:
            abort(400, message=f"Preferred channel must be one of {VALID_CHANNELS}")
        
        # Validate available_channels is a list
        if not isinstance(available, list):
            abort(400, message="Available channels must be a list")
        
        # Validate all available channels are valid
        if any(ch not in VALID_CHANNELS for ch in available):
            abort(400, message=f"Available channels can only include: {VALID_CHANNELS}")
        
        # Validate preferred channel is in available channels
        if preferred not in available:
            abort(400, message="Preferred channel must be in available_channels")
        
        # Validate no duplicate channels in available_channels
        if len(set(available)) != len(available):
            abort(400, message="Available channels must not contain duplicates")

        # Create new user object
        new_user = {
            'id': user_id_counter,
            'name': args['name'],
            'preferred_channel': preferred,
            'available_channels': available
        }
        
        # Add user to storage and increment counter
        users.append(new_user)
        user_id_counter += 1
        
        print(f"👤 New user created: {new_user['name']} (ID: {new_user['id']})")
        return new_user, 201


class Notifications(Resource):
    """
    Resource for managing notifications in the system.
    
    Handles notification sending with automatic channel fallback using
    the Chain of Responsibility pattern.
    """
    
    @marshal_with(notificationFields)
    def get(self):
        """
        Retrieve all sent notifications.
        ---
        tags:
          - Notifications
        summary: Get all notifications
        description: Returns a list of all notifications (both successful and failed final attempts)
        responses:
          200:
            description: List of notifications retrieved successfully
        """
        return notifications

    @marshal_with(notificationFields)
    def post(self):
        """
        Send a notification to a user.
        ---
        tags:
          - Notifications
        summary: Send a notification
        description: |
          Sends a notification to a specified user using the Chain of Responsibility pattern.
          The system will attempt delivery via all available channels until successful or all fail.
          All attempts (successful and failed) are logged in the notification history.
        parameters:
          - in: body
            name: notification
            description: Notification data
            required: true
            schema:
              type: object
              required:
                - user_name
                - message
                - priority
              properties:
                user_name:
                  type: string
                  description: Name of the user to send notification to
                  example: "John Doe"
                message:
                  type: string
                  description: Content of the notification
                  example: "Your order has been shipped"
                priority:
                  type: string
                  description: Priority level of the notification
                  example: "medium"
                  enum: ["high", "medium", "low"]
        responses:
          201:
            description: Notification sent successfully
          404:
            description: User not found
          500:
            description: All delivery attempts failed
        """
        global notification_id_counter
        args = notification_args.parse_args()
        
        # Find the target user by name
        user = next((u for u in users if u['name'] == args['user_name']), None)

        if not user:
            abort(404, message="User not found")

        print(f"📨 Attempting to send notification to {user['name']}")
        print(f"   Message: {args['message']}")
        print(f"   Priority: {args['priority']}")

        # Create list of channels to try: preferred channel first, then others
        channels_to_try = [user['preferred_channel']] + [
            c for c in user['available_channels'] 
            if c != user['preferred_channel']
        ]
        
        delivered_via = None
        attempt_number = 1
        print(f"   Trying channels in order: {channels_to_try}")

        # Attempt delivery through each channel using Chain of Responsibility
        for channel in channels_to_try:
            print(f"   Attempting delivery via {channel} (attempt #{attempt_number})...")
            delivered_via = handler_chain.handle(
                channel, user, args['message'], 
                notification_id_counter, args['priority'], attempt_number
            )
            if delivered_via:
                print(f"Successfully delivered via {delivered_via}")
                break
            else:
                print(f"Failed to deliver via {channel}")
            attempt_number += 1

        # Create notification record (regardless of success or failure)
        new_notification = {
            'id': notification_id_counter,
            'user_name': user['name'],
            'message': args['message'],
            'priority': args['priority'],
            'delivered_via': delivered_via if delivered_via else "FAILED",
            'timestamp': datetime.now().isoformat(),
            'total_attempts': attempt_number - 1,
            'success': delivered_via is not None
        }
        
        # Store notification and increment counter
        notifications.append(new_notification)
        notification_id_counter += 1

        # If all delivery attempts failed, return error but keep the record
        if not delivered_via:
            print(f"All delivery attempts failed for {user['name']}")
            abort(500, message="All delivery attempts failed")
        
        return new_notification, 201


class NotificationHistory(Resource):
    """
    Resource for retrieving detailed notification history.
    
    Shows all individual delivery attempts, both successful and failed.
    """
    
    @marshal_with(historyFields)
    def get(self):
        """
        Retrieve complete notification history.
        ---
        tags:
          - Notification History
        summary: Get complete notification history
        description: |
          Returns a detailed history of all notification delivery attempts, 
          including both successful and failed attempts for each notification.
        responses:
          200:
            description: Complete notification history retrieved successfully
            schema:
              type: array
              items:
                type: object
                properties:
                  id:
                    type: integer
                    description: Unique history entry identifier
                  notification_id:
                    type: integer
                    description: ID of the related notification
                  user_name:
                    type: string
                    description: Name of the target user
                  message:
                    type: string
                    description: Message content
                  priority:
                    type: string
                    enum: ["high", "medium", "low"]
                  channel:
                    type: string
                    enum: ["email", "sms", "whatsapp"]
                    description: Channel attempted
                  success:
                    type: boolean
                    description: Whether this attempt was successful
                  timestamp:
                    type: string
                    format: date-time
                    description: When the attempt was made
                  attempt_number:
                    type: integer
                    description: Attempt number in sequence
        """
        return notification_history



# ------------------------
# ROUTE REGISTRATION
# ------------------------

# Register API resources with their endpoints
api.add_resource(Users, '/users/')
api.add_resource(Notifications, '/notifications/send')
api.add_resource(NotificationHistory, '/notifications/history')


@app.route('/')
def home():
    """
    Home endpoint with API information and links.
    
    Returns:
        str: HTML page with API documentation links
    """
    return """
    <h1>Sistema de Notificaciones - Chain of Responsability</h1>
    <p><strong>Presentado por:</strong> Maria Paula Carvajal Martinez</p>
    <p><strong>Email:</strong> marcarvajalma@unal.edu.co</p>
    
    <h2>Endpoints Disponibles</h2>
    <ul>
        <li><strong>GET/POST /users/</strong> - Gestión de usuarios</li>
        <li><strong>GET/POST /notifications/send</strong> - Envío de notificaciones</li>
        <li><strong>GET /notifications/history</strong> - Historial de entregas</li>
    </ul>
    
    <h2>Documentation</h2>
    <ul>
        <li><a href="/swagger/">Documentación de Swagger</a></li>
    </ul>
    
    <h2>Patrón Chain of Responsibility</h2>
    <p>Este sistema utiliza el patrón Chain of Responsibility para manejar el envío de notificaciones de forma secuencial y tolerante a fallos:</p>
    <ul>
      <li><strong>EmailHandler</strong> -Intenta enviar la notificación por correo electrónico</li>
      <li><strong>SmsHandler</strong> -Si falla el correo, intenta enviarla por SMS</li>
      <li><strong>WhatsAppHandler</strong> -Si falla el SMS, intenta enviarla por WhatsApp</li>
    </ul>
    <p>
      Cada handler decide si puede manejar la notificación. Si no puede, la pasa al siguiente en la cadena.
    </p>

    """


# ------------------------
# APPLICATION ENTRY POINT
# ------------------------

if __name__ == '__main__':
    print("Documentación disponible en: http://localhost:5000/swagger/")
    
    # Run the Flask application in debug mode
    app.run(debug=True)