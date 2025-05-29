from __future__ import annotations
from typing import Optional
from abc import ABC, abstractmethod
from app.utils.logger import Logger

class NotificationHandler(ABC):
    def __init__(self):
        self._next_handler = None
        self.logger = Logger()

    def set_next(self, handler: NotificationHandler) -> NotificationHandler:
        """Chains the next handler in the responsibility chain."""
        self._next_handler = handler
        return handler  # Allows chaining: handler1.set_next(handler2).set_next(handler3)

    @abstractmethod
    def handle(self, user_name: str, message: str, channel: str, remaining_channels: list) -> Optional[str]:
        """
        Main method to be implemented by each concrete handler.
        This is where each handler tries to send the notification via its channel.
        """
        pass

    def _attempt_next(self, user_name: str, message: str, remaining_channels: list):
        """
        Attempts to delegate the notification to the next handler in the chain,
        if one exists and there are remaining channels to try.
        """
        if self._next_handler and remaining_channels:
            next_channel = remaining_channels[0]
            return self._next_handler.handle(user_name, message, next_channel, remaining_channels[1:])
        else:
            # If there's no next handler or no channels left, log a failure
            self.logger.log(f"Error: {user_name} could not be notified, no more channels available.")