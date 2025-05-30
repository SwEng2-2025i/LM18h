from abc import ABC, abstractmethod
from random import choice

class NotificationHandler(ABC):
    @abstractmethod
    def set_next(self, handler):
        pass

    @abstractmethod
    def handle(self, user, message, priority):
        pass

class AbstractHandler(NotificationHandler):
    _next_handler = None

    def set_next(self, handler):
        self._next_handler = handler
        return handler

    def handle(self, user, message, priority):
        if self._next_handler:
            return self._next_handler.handle(user, message, priority)
        return None