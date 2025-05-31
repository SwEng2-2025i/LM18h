from models.notification import Notification
from services.notification_handler import EmailHandler, SMSHandler, ConsoleHandler
from services.logger import Logger

class NotificationService:
    def __init__(self):
        self.logger = Logger()
        self._setup_handlers()

    def _setup_handlers(self):
        self.email_handler = EmailHandler()
        self.sms_handler = SMSHandler()
        self.console_handler = ConsoleHandler()

        # Set up the chain of responsibility
        self.email_handler.set_next(self.sms_handler).set_next(self.console_handler)

    def send_notification(self, user_name, message, priority="normal"):
        from services.user_service import UserService
        user_service = UserService()
        user = user_service.get_user(user_name)
        
        if not user:
            raise ValueError(f"User {user_name} not found")

        notification = Notification(user_name, message, priority)
        
        # Start with the preferred channel
        preferred_handler = self._get_handler_for_channel(user.preferred_channel)
        if preferred_handler:
            self.logger.log(f"Attempting to send notification to {user_name} via {user.preferred_channel}")
            success = preferred_handler.handle(notification, user)
        else:
            success = self.email_handler.handle(notification, user)

        return notification.to_dict()

    def _get_handler_for_channel(self, channel):
        handlers = {
            "email": self.email_handler,
            "sms": self.sms_handler,
            "console": self.console_handler
        }
        return handlers.get(channel) 