"""
Notification Handler implementing Chain of Responsibility pattern.

Handles delivery attempts through different channels with fallback mechanism.
"""

import random

class NotificationHandler:
    def __init__(self, channel):
        self.channel = channel
        self.next_handler = None

    def set_next(self, next_handler):
        self.next_handler = next_handler
        return next_handler

    def handle(self, user_name, message, priority):
        success = random.choice([True, False])
        if success:
            return {
                "status": "Notification registered",
                "to": user_name,
                "message": message,
                "priority": priority,
                "channel": self.channel
            }
        elif self.next_handler:
            return self.next_handler.handle(user_name, message, priority)
        else:
            return {
                "status": "Notification failed",
                "to": user_name,
                "message": message,
                "priority": priority,
                "channel": None
            }
