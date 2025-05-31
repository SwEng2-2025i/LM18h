import random
from abc import ABC, abstractmethod

class NotificationHandler(ABC):
    def __init__(self):
        self._next_handler = None

    def set_next(self, handler):
        self._next_handler = handler
        return handler

    @abstractmethod
    def handle(self, notification, user):
        pass

    def _simulate_delivery(self):
        return random.choice([True, False])

class EmailHandler(NotificationHandler):
    def handle(self, notification, user):
        if "email" in user.available_channels:
            success = self._simulate_delivery()
            notification.add_delivery_attempt("email", success)
            if success:
                return True
        if self._next_handler:
            return self._next_handler.handle(notification, user)
        return False

class SMSHandler(NotificationHandler):
    def handle(self, notification, user):
        if "sms" in user.available_channels:
            success = self._simulate_delivery()
            notification.add_delivery_attempt("sms", success)
            if success:
                return True
        if self._next_handler:
            return self._next_handler.handle(notification, user)
        return False

class ConsoleHandler(NotificationHandler):
    def handle(self, notification, user):
        if "console" in user.available_channels:
            success = self._simulate_delivery()
            notification.add_delivery_attempt("console", success)
            if success:
                return True
        if self._next_handler:
            return self._next_handler.handle(notification, user)
        return False 