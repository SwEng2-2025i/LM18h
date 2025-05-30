from handlers.init import AbstractHandler
from utils.logger import Logger
from random import choice

class EmailHandler(AbstractHandler):
    def handle(self, user, message, priority):
        if "email" in user.available_channels:
            logger = Logger()
            logger.log(f"Attempting to send email to {user.name}")
            
            # Simulate random success/failure
            success = choice([True, False])
            
            if success:
                logger.log(f"Email sent successfully to {user.name}")
                return {"status": "success", "channel": "email", "message": message}
            else:
                logger.log(f"Email failed for {user.name}, trying next channel")
                return super().handle(user, message, priority)
        return super().handle(user, message, priority)