from handlers.init import AbstractHandler
from utils.logger import Logger

class ConsoleHandler(AbstractHandler):
    def handle(self, user, message, priority):
        if "console" in user.available_channels:
            logger = Logger()
            logger.log(f"Attempting to send console notification to {user.name}")
            
            # Console always succeeds as a fallback
            logger.log(f"Console notification displayed for {user.name}")
            return {"status": "success", "channel": "console", "message": message}
        return super().handle(user, message, priority)