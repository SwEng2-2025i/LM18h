from handlers.base_handler import BaseHandler
from logger import NotificationLogger
import random

class ConsoleHandler(BaseHandler):
    def handle(self, user, message):
        logger = NotificationLogger()

        if "console" in user['available']:
            print(f"[ConsoleHandler] Printing message to console: {message}")
            success = random.choice([True, False])
            logger.log_attempt(user, "console", message, success)
            if success:
                print("[ConsoleHandler] Console delivery simulated successfully.")
                return True
            print("[ConsoleHandler] Console delivery failed.")

        return self.next_handler.handle(user, message) if self.next_handler else False
