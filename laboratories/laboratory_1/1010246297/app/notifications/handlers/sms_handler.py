from app.notifications.handlers.base_handler import NotificationHandler  # Asegúrate de importar la correcta
import random

class SMSHandler(NotificationHandler):
    def handle(self, user_name: str, message: str, channel: str, remaining_channels: list) -> str:
        if channel.lower() == "sms":
            success = random.choice([True, False])
            if success:
                self.logger.log(f"SMS sent to {user_name}: {message}")
                return True
            else:
                self.logger.log(f"Failed to send SMS to {user_name}. Trying next channel...")
                return self._attempt_next(user_name, message, remaining_channels)
        else:
            return self._attempt_next(user_name, message, remaining_channels)
