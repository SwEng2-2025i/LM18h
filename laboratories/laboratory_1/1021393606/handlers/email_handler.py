from handlers.base_handler import BaseHandler
from logger import NotificationLogger
import random

class EmailHandler(BaseHandler):
    def handle(self, user, message):
        logger = NotificationLogger()

        if "email" in user['available_channels']:
            print(f"[EmailHandler] Sending email: {message}")
            success = random.choice([True, False])
            logger.log_attempt(user, "email", message, success)
            if success:
                return True
        # Si falla o el canal no está disponible, pasa al siguiente handler
        return self.next_handler.handle(user, message) if self.next_handler else False
