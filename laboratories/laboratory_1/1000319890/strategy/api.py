from flask import Flask, request
from flask_restful import Resource, Api, reqparse, fields, marshal_with, abort
from flasgger import Swagger, swag_from
import random
from abc import ABC, abstractmethod
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
        "title": "Notification Delivery API - Strategy Pattern",
        "description": "A Flask REST API implementing Strategy pattern for notification delivery with complete attempt tracking and statistics",
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

# ===========================
# DATA STRUCTURES
# ===========================

# In-memory data storage - In production, this would be replaced with a database
users = []  # List to store user objects
notifications = []  # List to store notification objects
notification_history = []  # List to store all notification attempts (successful and failed)

# Global counters for unique IDs
user_id_counter = 1
notification_id_counter = 1
history_id_counter = 1

# Valid communication channels supported by the system
VALID_CHANNELS = {"email", "sms", "whatsapp"}

# ===========================
# REQUEST PARSERS
# ===========================

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

# ===========================
# OUTPUT FIELD DEFINITIONS
# ===========================

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

# ===========================
# UTILITY FUNCTIONS
# ===========================

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

# ===========================
# STRATEGY PATTERN IMPLEMENTATION
# ===========================

class NotificationStrategy(ABC):
    """
    Abstract base class for the Strategy pattern.
    
    Defines the interface that all concrete delivery strategies must implement.
    Each strategy encapsulates a specific delivery algorithm/method.
    """
    
    @abstractmethod
    def deliver(self, user, message, notification_id, priority, attempt_number):
        """
        Abstract method to deliver a notification.
        
        Args:
            user (dict): User object containing delivery preferences
            message (str): Message content to deliver
            notification_id (int): ID of the notification
            priority (str): Priority level
            attempt_number (int): Current attempt number
            
        Returns:
            bool: True if delivery successful, False otherwise
        """
        pass
    
    @abstractmethod
    def get_channel_name(self):
        """
        Abstract method to get the channel name for this strategy.
        
        Returns:
            str: The name of the communication channel
        """
        pass


class EmailStrategy(NotificationStrategy):
    """
    Concrete strategy for email delivery.
    
    Implements the email delivery algorithm with simulated success/failure.
    """
    
    def deliver(self, user, message, notification_id, priority, attempt_number):
        """
        Deliver notification via email.
        
        Args:
            user (dict): Target user information
            message (str): Message to deliver
            notification_id (int): ID of the notification
            priority (str): Priority level
            attempt_number (int): Current attempt number
            
        Returns:
            bool: True if email delivery successful, False otherwise
        """
        print(f"Attempting email delivery to {user['name']}")
        
        # Simulate random delivery success/failure for demonstration
        # In production, this would integrate with actual email service (SendGrid, AWS SES, etc.)
        success = random.choice([True, False])
        
        # Log the attempt
        log_notification_attempt(
            notification_id, user['name'], message, priority, 
            'email', success, attempt_number
        )
        
        if success:
            print(f"Email sent successfully to {user['name']}")
            return True
        else:
            print(f"Email delivery failed for {user['name']}")
            return False
    
    def get_channel_name(self):
        """Get the channel name for email strategy."""
        return 'email'


class SmsStrategy(NotificationStrategy):
    """
    Concrete strategy for SMS delivery.
    
    Implements the SMS delivery algorithm with simulated success/failure.
    """
    
    def deliver(self, user, message, notification_id, priority, attempt_number):
        """
        Deliver notification via SMS.
        
        Args:
            user (dict): Target user information
            message (str): Message to deliver
            notification_id (int): ID of the notification
            priority (str): Priority level
            attempt_number (int): Current attempt number
            
        Returns:
            bool: True if SMS delivery successful, False otherwise
        """
        print(f"Attempting SMS delivery to {user['name']}")
        
        # Simulate random delivery success/failure for demonstration
        # In production, this would integrate with SMS service (Twilio, AWS SNS, etc.)
        success = random.choice([True, False])
        
        # Log the attempt
        log_notification_attempt(
            notification_id, user['name'], message, priority, 
            'sms', success, attempt_number
        )
        
        if success:
            print(f"SMS sent successfully to {user['name']}")
            return True
        else:
            print(f"SMS delivery failed for {user['name']}")
            return False
    
    def get_channel_name(self):
        """Get the channel name for SMS strategy."""
        return 'sms'


class WhatsAppStrategy(NotificationStrategy):
    """
    Concrete strategy for WhatsApp delivery.
    
    Implements the WhatsApp delivery algorithm with simulated success/failure.
    """
    
    def deliver(self, user, message, notification_id, priority, attempt_number):
        """
        Deliver notification via WhatsApp.
        
        Args:
            user (dict): Target user information
            message (str): Message to deliver
            notification_id (int): ID of the notification
            priority (str): Priority level
            attempt_number (int): Current attempt number
            
        Returns:
            bool: True if WhatsApp delivery successful, False otherwise
        """
        print(f"Attempting WhatsApp delivery to {user['name']}")
        
        # Simulate random delivery success/failure for demonstration
        # In production, this would integrate with WhatsApp Business API
        success = random.choice([True, False])
        
        # Log the attempt
        log_notification_attempt(
            notification_id, user['name'], message, priority, 
            'whatsapp', success, attempt_number
        )
        
        if success:
            print(f"WhatsApp sent successfully to {user['name']}")
            return True
        else:
            print(f"WhatsApp delivery failed for {user['name']}")
            return False
    
    def get_channel_name(self):
        """Get the channel name for WhatsApp strategy."""
        return 'whatsapp'


class NotificationContext:
    """
    Context class for the Strategy pattern.
    
    This class maintains a reference to a strategy object and delegates
    the delivery work to the strategy. It also handles strategy selection
    and fallback logic with complete attempt tracking.
    """
    
    def __init__(self):
        """Initialize the context with available strategies."""
        # Dictionary mapping channel names to their corresponding strategies
        self.strategies = {
            'email': EmailStrategy(),
            'sms': SmsStrategy(),
            'whatsapp': WhatsAppStrategy()
        }
        self.current_strategy = None
    
    def set_strategy(self, channel):
        """
        Set the delivery strategy based on channel name.
        
        Args:
            channel (str): Name of the communication channel
            
        Returns:
            bool: True if strategy was set successfully, False if channel invalid
        """
        if channel in self.strategies:
            self.current_strategy = self.strategies[channel]
            print(f"Strategy set to {channel}")
            return True
        else:
            print(f"Invalid channel: {channel}")
            return False
    
    def deliver_notification(self, user, message, notification_id, priority, attempt_number):
        """
        Deliver notification using the current strategy.
        
        Args:
            user (dict): Target user information
            message (str): Message to deliver
            notification_id (int): ID of the notification
            priority (str): Priority level
            attempt_number (int): Current attempt number
            
        Returns:
            tuple: (success: bool, channel_used: str or None)
        """
        if not self.current_strategy:
            print("No strategy set for delivery")
            return False, None
        
        success = self.current_strategy.deliver(user, message, notification_id, priority, attempt_number)
        channel_used = self.current_strategy.get_channel_name() if success else None
        
        return success, channel_used
    
    def deliver_with_fallback(self, user, message, notification_id, priority):
        """
        Deliver notification with intelligent fallback strategy.
        
        This method implements the core business logic:
        1. Try preferred channel first
        2. If that fails, try other available channels
        3. Log all attempts (successful and failed)
        4. Return the successful channel and attempt count
        
        Args:
            user (dict): Target user with channel preferences
            message (str): Message to deliver
            notification_id (int): ID of the notification
            priority (str): Priority level
            
        Returns:
            tuple: (channel_name: str or None, total_attempts: int)
        """
        print(f"Starting Strategy Pattern delivery process for {user['name']}")
        print(f"Message: {message}")
        print(f"Priority: {priority}")
        print(f"Preferred channel: {user['preferred_channel']}")
        print(f"Available channels: {user['available_channels']}")
        
        # Create list of channels to try: preferred first, then others
        channels_to_try = [user['preferred_channel']] + [
            ch for ch in user['available_channels'] 
            if ch != user['preferred_channel']
        ]
        
        print(f"Trying channels in order: {channels_to_try}")
        
        attempt_number = 1
        
        # Try each channel using the appropriate strategy
        for channel in channels_to_try:
            print(f"Attempting delivery via {channel} (attempt #{attempt_number})...")
            
            # Set the strategy for the current channel
            if self.set_strategy(channel):
                success, channel_used = self.deliver_notification(
                    user, message, notification_id, priority, attempt_number
                )
                
                if success:
                    print(f"Successfully delivered via {channel_used}")
                    return channel_used, attempt_number
                else:
                    print(f"Failed to deliver via {channel}")
            else:
                print(f"Invalid strategy for channel: {channel}")
                # Still log failed attempt for invalid strategy
                log_notification_attempt(
                    notification_id, user['name'], message, priority, 
                    channel, False, attempt_number
                )
            
            attempt_number += 1
        
        # All delivery attempts failed
        print(f"All delivery strategies failed for {user['name']}")
        return None, attempt_number - 1


# Create a global notification context instance
notification_context = NotificationContext()

# ===========================
# API RESOURCES
# ===========================

class Users(Resource):
    """
    Resource for managing users in the notification system.
    
    Handles user creation and retrieval with communication preferences.
    Uses the same interface as the Chain of Responsibility version.
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
        description: Creates a new user with communication preferences and validates input data using Strategy pattern for future notifications
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
                  description: User's preferred communication channel (primary strategy)
                  example: "email"
                  enum: ["email", "sms", "whatsapp"]
                available_channels:
                  type: array
                  items:
                    type: string
                    enum: ["email", "sms", "whatsapp"]
                  description: List of available communication channels (fallback strategies)
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
        print(f"   Primary strategy: {new_user['preferred_channel']}")
        print(f"   Fallback strategies: {[ch for ch in new_user['available_channels'] if ch != new_user['preferred_channel']]}")
        
        return new_user, 201


class Notifications(Resource):
    """
    Resource for managing notifications in the system.
    
    Handles notification sending with automatic channel fallback using
    the Strategy pattern with complete attempt tracking.
    """
    
    @marshal_with(notificationFields)
    def get(self):
        """
        Retrieve all sent notifications.
        ---
        tags:
          - Notifications
        summary: Get all notifications
        description: Returns a list of all notifications (both successful and failed final attempts) with complete delivery information
        responses:
          200:
            description: List of notifications retrieved successfully
        """
        return notifications

    @marshal_with(notificationFields)
    def post(self):
        """
        Send a notification to a user using Strategy pattern with complete tracking.
        ---
        tags:
          - Notifications
        summary: Send a notification using Strategy pattern
        description: |
          Sends a notification to a specified user using the Strategy design pattern.
          The system will dynamically select and switch between delivery strategies,
          logging all attempts (successful and failed) in the notification history.
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
            description: Notification sent successfully using one of the strategies
          404:
            description: User not found
          500:
            description: All delivery strategies failed
        """
        global notification_id_counter
        args = notification_args.parse_args()
        
        # Find the target user by name
        user = next((u for u in users if u['name'] == args['user_name']), None)

        if not user:
            abort(404, message="User not found")

        print(f"🚀 Strategy Pattern: Starting notification delivery")
        
        # Use the notification context to deliver with fallback strategies
        delivered_via, total_attempts = notification_context.deliver_with_fallback(
            user, args['message'], notification_id_counter, args['priority']
        )

        # Create notification record (regardless of success or failure)
        new_notification = {
            'id': notification_id_counter,
            'user_name': user['name'],
            'message': args['message'],
            'priority': args['priority'],
            'delivered_via': delivered_via if delivered_via else "FAILED",
            'timestamp': datetime.now().isoformat(),
            'total_attempts': total_attempts,
            'success': delivered_via is not None
        }
        
        # Store notification and increment counter
        notifications.append(new_notification)
        notification_id_counter += 1

        # If all strategies failed, return error but keep the record
        if not delivered_via:
            print(f"All delivery strategies failed for {user['name']}")
            abort(500, message="All delivery strategies failed")
        
        print(f"Notification successfully delivered using {delivered_via} strategy")
        
        return new_notification, 201


class NotificationHistory(Resource):
    """
    Resource for retrieving detailed notification history.
    
    Shows all individual delivery attempts using different strategies,
    both successful and failed.
    """
    
    @marshal_with(historyFields)
    def get(self):
        """
        Retrieve complete notification history.
        ---
        tags:
          - Notification History
        summary: Get complete notification history with Strategy pattern details
        description: |
          Returns a detailed history of all notification delivery attempts using various strategies, 
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
                    description: Strategy/channel attempted
                  success:
                    type: boolean
                    description: Whether this strategy attempt was successful
                  timestamp:
                    type: string
                    format: date-time
                    description: When the strategy attempt was made
                  attempt_number:
                    type: integer
                    description: Strategy attempt number in sequence
        """
        return notification_history


class NotificationStats(Resource):
    """
    Resource for retrieving notification statistics with Strategy pattern insights.
    """
    
    def get(self):
        """
        Get notification delivery statistics with Strategy pattern analysis.
        ---
        tags:
          - Statistics
        summary: Get notification statistics with Strategy pattern insights
        description: Returns statistics about notification delivery success rates by strategy/channel with Strategy pattern specific metrics
        responses:
          200:
            description: Statistics retrieved successfully
            schema:
              type: object
              properties:
                total_notifications:
                  type: integer
                  description: Total number of notifications sent
                successful_notifications:
                  type: integer
                  description: Number of successfully delivered notifications
                failed_notifications:
                  type: integer
                  description: Number of failed notifications
                success_rate:
                  type: number
                  description: Overall success rate percentage
                strategy_stats:
                  type: object
                  description: Statistics by strategy/channel
                total_attempts:
                  type: integer
                  description: Total strategy attempts made
                average_attempts_per_notification:
                  type: number
                  description: Average number of strategy attempts per notification
        """
        total_notifications = len(notifications)
        successful_notifications = len([n for n in notifications if n['success']])
        failed_notifications = total_notifications - successful_notifications
        success_rate = (successful_notifications / total_notifications * 100) if total_notifications > 0 else 0
        
        # Strategy statistics
        strategy_stats = {}
        for channel in VALID_CHANNELS:
            strategy_attempts = [h for h in notification_history if h['channel'] == channel]
            strategy_successes = [h for h in strategy_attempts if h['success']]
            strategy_stats[channel] = {
                'total_attempts': len(strategy_attempts),
                'successful_attempts': len(strategy_successes),
                'success_rate': (len(strategy_successes) / len(strategy_attempts) * 100) if strategy_attempts else 0,
                'failed_attempts': len(strategy_attempts) - len(strategy_successes)
            }
        
        # Calculate average attempts per notification
        total_attempts = len(notification_history)
        avg_attempts = (total_attempts / total_notifications) if total_notifications > 0 else 0
        
        return {
            'total_notifications': total_notifications,
            'successful_notifications': successful_notifications,
            'failed_notifications': failed_notifications,
            'success_rate': round(success_rate, 2),
            'strategy_stats': strategy_stats,
            'total_attempts': total_attempts,
            'average_attempts_per_notification': round(avg_attempts, 2),
            'pattern_type': 'Strategy Pattern'
        }


# ===========================
# ROUTE REGISTRATION
# ===========================

# Register API resources with their endpoints
api.add_resource(Users, '/users/')
api.add_resource(Notifications, '/notifications/send')
api.add_resource(NotificationHistory, '/notifications/history')
api.add_resource(NotificationStats, '/notifications/stats')


@app.route('/')
def home():
    """
    Home endpoint with API information and links.
    
    Returns:
        str: HTML page with API documentation links
    """
    return """
    <h1>Flask REST API with Strategy Pattern</h1>
    <h2>Documentation</h2>
    <ul>
        <li><a href="/swagger/">Swagger UI Documentation</a></li>
        <li><a href="/apispec.json">API Specification (JSON)</a></li>
    </ul>
    <h2>Available Endpoints</h2>
    <ul>
        <li><strong>GET/POST</strong> <a href="/users/">/users/</a> - User management</li>
        <li><strong>GET/POST</strong> <a href="/notifications/send">/notifications/send</a> - Notification delivery</li>
        <li><strong>GET</strong> <a href="/notifications/history">/notifications/history</a> - Complete delivery history</li>
        <li><strong>GET</strong> <a href="/notifications/stats">/notifications/stats</a> - Delivery statistics</li>
    </ul>
    """


# ===========================
# APPLICATION ENTRY POINT
# ===========================

if __name__ == '__main__':
    app.run(debug=True)