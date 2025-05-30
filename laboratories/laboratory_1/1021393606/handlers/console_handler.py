from handlers.base_handler import BaseHandler
from logger import NotificationLogger
import random

class ConsoleHandler(BaseHandler):
    def handle(self, user, message):
        logger = NotificationLogger()

        if "console" in user['available_channels']:
            print(f"[ConsoleHandler] Sending console message: {message}")
            success = random.choice([True, False])
            logger.log_attempt(user, "console", message, success)
            if success:
                return True
        # Si falla o el canal no está disponible, pasa al siguiente handler
        return self.next_handler.handle(user, message) if self.next_handler else False
