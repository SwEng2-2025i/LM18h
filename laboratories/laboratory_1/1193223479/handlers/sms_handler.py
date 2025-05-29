from handlers.base_handler import BaseHandler
from logger import NotificationLogger
import random

class SMSHandler(BaseHandler):
    def handle(self, user, message):
        logger = NotificationLogger()

        if "sms" in user['available']:
            print(f"[SMSHandler] Trying to send SMS: {message}")
            success = random.choice([True, False])
            logger.log_attempt(user, "sms", message, success)
            if success:
                print("[SMSHandler] SMS sent successfully.")
                return True
            print("[SMSHandler] SMS failed.")

        return self.next_handler.handle(user, message) if self.next_handler else False

