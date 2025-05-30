import random
from services.logger import Logger

class NotificationChannel:
    def __init__(self, name):
        self.name = name
        self.next_channel = None

    def set_next(self, channel):
        self.next_channel = channel
        return channel  # Permite encadenamiento fluido

    def handle(self, message):
        return self._attempt_handle(message).handle(message)

    def _attempt_handle(self, message):
        if self.can_handle():
            return HandlerResult(lambda: self.process(message))
        return self.next_channel or FallbackHandler()

    def can_handle(self):
        return random.choice([True, False])

    def process(self, message):
        Logger().log(f"[{self.name}] Successfully sent message: '{message}'")
        return f"Sent via {self.name}"

# Esta clase encapsula el resultado como callable para evitar condicionales
class HandlerResult:
    def __init__(self, handler_function):
        self._handler_function = handler_function

    def handle(self, message):
        return self._handler_function()

# Fallback final en la cadena
class FallbackHandler:
    def handle(self, message):
        Logger().log(f"All channels failed for message: '{message}'")
        return "All channels failed"
