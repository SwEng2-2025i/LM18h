# app/patterns/channel_handlers.py

import random
from app.utils.logger import NotificationLogger

logger = NotificationLogger()

class ChannelHandler:
    def __init__(self, channel_name):
        self.channel_name = channel_name
        self.next_handler = None

    def set_next(self, handler):
        self.next_handler = handler
        return handler

    def handle(self, user, message):
        print(f"Trying to send via {self.channel_name}...")

        success = random.choice([True, False])
        status = "success" if success else "failed"
        logger.log(user.name, self.channel_name, status)

        if success:
            print(f" Sent to {user.name} via {self.channel_name}")
            return {
                "status": "success",
                "channel": self.channel_name,
                "message": message
            }
        else:
            print(f" Failed via {self.channel_name}")
            if self.next_handler:
                return self.next_handler.handle(user, message)
            else:
                return {
                    "status": "failed",
                    "message": f"All channels failed for {user.name}"
                }
