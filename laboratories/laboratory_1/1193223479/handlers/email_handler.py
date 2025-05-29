from handlers.base_handler import BaseHandler
from logger import NotificationLogger
import random

class EmailHandler(BaseHandler):
    def handle(self, user, message):
        logger = NotificationLogger()

        if "email" in user['available']:
            print(f"[EmailHandler] Trying to send email: {message}")
            success = random.choice([True, False])
            logger.log_attempt(user, "email", message, success)
            if success:
                print("[EmailHandler] Email sent successfully.")
                return True
            print("[EmailHandler] Email failed.")

        return self.next_handler.handle(user, message) if self.next_handler else False

