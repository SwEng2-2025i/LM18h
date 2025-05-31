# handlers.py

import random
from app.logger import LoggerSingleton


class NotificationHandler:
    def __init__(self, channel):
        self.channel = channel
        self.next_handler = None
        self.logger = LoggerSingleton()

    def set_next(self, handler):
        self.next_handler = handler
        return handler

    def handle(self, message, channel):
        if self.channel == channel:
            success = random.choice([True, False])
            self.logger.log(f"Trying {self.channel.upper()} channel: {'Success' if success else 'Failed'}")
            if success:
                return True
        if self.next_handler:
            return self.next_handler.handle(message, self.next_handler.channel)
        self.logger.log("All channels failed.")
        return False
