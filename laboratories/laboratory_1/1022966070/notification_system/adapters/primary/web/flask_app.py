from flask import Flask, send_from_directory
from .controllers import UserController, NotificationController
from notification_system.adapters.secondary.notification_handlers import (ConsoleNotificationHandler, EmailNotificationHandler, SMSNotificationHandler)
from ...secondary.in_memory_user_repository import InMemoryUserRepository
from ....domain.services import NotificationService

from ....application.use_cases import UserUseCases, NotificationUseCases
from .swagger import swagger_ui_blueprint, SWAGGER_URL
import logging 



def create_app():
    app = Flask(__name__, static_folder='static')
    logging.basicConfig(level=logging.INFO)
    # Setup dependencies
    user_repository = InMemoryUserRepository()
    handlers = [
        ConsoleNotificationHandler(),
        EmailNotificationHandler(),
        SMSNotificationHandler()
    ]
    notification_service = NotificationService(handlers)
    
    user_use_cases = UserUseCases(user_repository)
    notification_use_cases = NotificationUseCases(user_repository, notification_service)
    
    user_controller = UserController(user_use_cases)
    notification_controller = NotificationController(notification_use_cases)
    
    # Register routes
    app.add_url_rule('/users', 'register_user', user_controller.register_user, methods=['POST'])
    app.add_url_rule('/users', 'list_users', user_controller.list_users, methods=['GET'])
    app.add_url_rule('/notifications/send', 'send_notification',
                    notification_controller.send_notification, methods=['POST'])
    
    # Add route to serve swagger.json
    @app.route('/static/swagger.json')
    def serve_swagger():
        return send_from_directory(app.static_folder, 'swagger.json')
    
    # Register Swagger UI blueprint
    app.register_blueprint(swagger_ui_blueprint, url_prefix=SWAGGER_URL)
    
    return app