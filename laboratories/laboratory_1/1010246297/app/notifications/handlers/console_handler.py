from app.notifications.handlers.base_handler import NotificationHandler
import random

class ConsoleHandler(NotificationHandler):
    def handle(self, user_name, message, channel, remaining_channels):
        if channel == "console":
            success = random.choice([True, False])
            if success:
                self.logger.log(f"Output console for {user_name}: {message}")
                return True
            else:
                self.logger.log(f"Failed console output to {user_name}. Trying next channel....")
                return self._attempt_next(user_name, message, remaining_channels)
        else:
            return self._attempt_next(user_name, message, remaining_channels)
