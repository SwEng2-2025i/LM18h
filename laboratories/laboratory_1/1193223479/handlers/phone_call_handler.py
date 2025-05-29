from handlers.base_handler import BaseHandler
from logger import NotificationLogger
import random

class PhoneCallHandler(BaseHandler):
    def handle(self, user, message):
        logger = NotificationLogger()

        if "phone" in user['available']:
            print(f"[PhoneCallHandler] Simulating phone call with message: {message}")
            success = random.choice([True, False])
            logger.log_attempt(user, "phone", message, success)
            if success:
                print("[PhoneCallHandler] Phone call delivered successfully.")
                return True
            print("[PhoneCallHandler] Phone call failed.")

        return self.next_handler.handle(user, message) if self.next_handler else False
