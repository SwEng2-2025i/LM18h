from app.notifications.handlers.email_handler import EmailHandler
from app.notifications.handlers.sms_handler import SMSHandler
from app.notifications.handlers.console_handler import ConsoleHandler
from app.utils.logger import Logger

class NotificationService:
    def __init__(self):
        self.logger = Logger()

    def get_supported_channels(self):
        return {"email", "sms", "console"}

    def send_notification(self, user, message, priority):
        # Initialize available notification handlers
        handlers = {
            "email": EmailHandler(),
            "sms": SMSHandler(),
            "console": ConsoleHandler()
        }

        # Build the preferred order: start with the user's main channel,
        # followed by the rest (fallbacks)
        preferred_order = [user.preferred_channel] + [
            channel for channel in user.available_channels if channel != user.preferred_channel
        ]

        # Link handlers following the preferred order
        current_handler = handlers[preferred_order[0]]
        head = current_handler  

        for next_channel in preferred_order[1:]:
            current_handler.set_next(handlers[next_channel])
            current_handler = handlers[next_channel]

        # Extract the first (preferred) channel and the rest for fallback
        first_channel = preferred_order[0]
        remaining_channels = preferred_order[1:]

        # Try to send the notification using the first handler in the chain
        success = head.handle(user.name, message, first_channel, remaining_channels)
        self.logger.log(
            f"Notification to {user.name} with priority '{priority}' sent: {'Success' if success else 'Failed'}"
        )
        return success
