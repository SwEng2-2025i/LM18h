from services.logger import Logger
import random

class NotificationChannel:
    def __init__(self, name):
        self.name = name
        self.next_channel = None

    def set_next(self, channel):
        self.next_channel = channel
        return channel

    def handle(self, message):
        if self.can_handle():
            return self.process(message)
        elif self.next_channel:
            return self.next_channel.handle(message)
        else:
            Logger().log(f"All channels failed for message: '{message}'")
            return "All channels failed"

    def can_handle(self):
        return random.choice([True, False])

    def process(self, message):
        Logger().log(f"[{self.name}] Successfully sent message: '{message}'")
        return f"Sent via {self.name}"
