from app.notifications.handlers.base_handler import NotificationHandler
import random

class EmailHandler(NotificationHandler):
    def handle(self, user_name, message, channel, remaining_channels):
        if channel == "email":
            success = random.choice([True, False])
            if success:
                self.logger.log(f"Email sent to {user_name}: {message}")
                return True
            else:
                self.logger.log(f"Failed to send email to {user_name}. Trying next channel...")
                return self._attempt_next(user_name, message, remaining_channels)
        else:
            return self._attempt_next(user_name, message, remaining_channels)
