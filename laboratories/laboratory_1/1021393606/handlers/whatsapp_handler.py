from handlers.base_handler import BaseHandler
from logger import NotificationLogger
import random

class WhatsAppHandler(BaseHandler):
    def handle(self, user, message):
        logger = NotificationLogger()

        if "whatsapp" in user['available_channels']:
            print(f"[WhatsAppHandler] Sending WhatsApp message: {message}")
            success = random.choice([True, False])
            logger.log_attempt(user, "whatsapp", message, success)
            if success:
                return True
        # Si falla o el canal no está disponible, pasa al siguiente handler
        return self.next_handler.handle(user, message) if self.next_handler else False
