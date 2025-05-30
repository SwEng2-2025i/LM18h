from handlers.init import AbstractHandler
from utils.logger import Logger
from random import choice

class SMSHandler(AbstractHandler):
    def handle(self, user, message, priority):
        if "sms" in user.available_channels:
            logger = Logger()
            logger.log(f"Attempting to send SMS to {user.name}")
            
            success = choice([True, False])
            
            if success:
                logger.log(f"SMS sent successfully to {user.name}")
                return {"status": "success", "channel": "sms", "message": message}
            else:
                logger.log(f"SMS failed for {user.name}, trying next channel")
                return super().handle(user, message, priority)
        return super().handle(user, message, priority)