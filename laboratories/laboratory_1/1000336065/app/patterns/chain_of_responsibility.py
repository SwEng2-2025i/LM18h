from abc import ABC, abstractmethod
import random
from app.patterns.logger import AppLogger
from app.models import User, NotificationData

class NotificationHandler(ABC):
    def __init__(self):
        self._next_handler: 'NotificationHandler' = None
        self.logger = AppLogger.get_instance()

    def set_next(self, handler: 'NotificationHandler') -> 'NotificationHandler':
        self._next_handler = handler
        return handler # Allows chaining like handler1.set_next(handler2).set_next(handler3)

    @abstractmethod
    def handle_notification(self, user: User, notification: NotificationData) -> bool:
        pass

    def _simulate_delivery(self, channel_name: str, user: User, notification: NotificationData) -> bool:
        """Simulates delivery attempt and logs it."""
        # Simulate failure: 50% chance of failure for simplicity
        # In a real system, this would involve actual API calls, etc.
        success = random.choice([True, False])
        
        status = "SUCCESS" if success else "FAILURE"
        self.logger.log_attempt(
            user_name=user.name,
            channel=channel_name,
            message=notification.message,
            status=status,
            priority=notification.priority
        )
        return success

class EmailHandler(NotificationHandler):
    CHANNEL_NAME = "email"

    def handle_notification(self, user: User, notification: NotificationData) -> bool:
        if self.CHANNEL_NAME in user.available_channels:
            print(f"Attempting to send notification to {user.name} via {self.CHANNEL_NAME}...")
            if self._simulate_delivery(self.CHANNEL_NAME, user, notification):
                print(f"Notification sent successfully to {user.name} via {self.CHANNEL_NAME}.")
                return True
            else:
                print(f"Failed to send notification to {user.name} via {self.CHANNEL_NAME}.")
                if self._next_handler:
                    return self._next_handler.handle_notification(user, notification)
        elif self._next_handler: # If email is not available for user, try next
            print(f"Channel {self.CHANNEL_NAME} not available for {user.name}, trying next.")
            return self._next_handler.handle_notification(user, notification)
        
        print(f"No further channels to try for {user.name} after {self.CHANNEL_NAME} attempt or unavailability.")
        return False

class SMSHandler(NotificationHandler):
    CHANNEL_NAME = "sms"

    def handle_notification(self, user: User, notification: NotificationData) -> bool:
        if self.CHANNEL_NAME in user.available_channels:
            print(f"Attempting to send notification to {user.name} via {self.CHANNEL_NAME}...")
            if self._simulate_delivery(self.CHANNEL_NAME, user, notification):
                print(f"Notification sent successfully to {user.name} via {self.CHANNEL_NAME}.")
                return True
            else:
                print(f"Failed to send notification to {user.name} via {self.CHANNEL_NAME}.")
                if self._next_handler:
                    return self._next_handler.handle_notification(user, notification)
        elif self._next_handler:
            print(f"Channel {self.CHANNEL_NAME} not available for {user.name}, trying next.")
            return self._next_handler.handle_notification(user, notification)

        print(f"No further channels to try for {user.name} after {self.CHANNEL_NAME} attempt or unavailability.")
        return False

class ConsoleHandler(NotificationHandler):
    CHANNEL_NAME = "console"

    def handle_notification(self, user: User, notification: NotificationData) -> bool:
        # Console is assumed to always be available if listed and always succeed
        if self.CHANNEL_NAME in user.available_channels:
            print(f"Attempting to send notification to {user.name} via {self.CHANNEL_NAME}...")
            # Console delivery always succeeds for simulation purposes
            self.logger.log_attempt(
                user_name=user.name,
                channel=self.CHANNEL_NAME,
                message=notification.message,
                status="SUCCESS",
                priority=notification.priority,
                details="Console output always succeeds."
            )
            print(f"CONSOLE NOTIFICATION for {user.name} ({notification.priority}): {notification.message}")
            return True
        elif self._next_handler:
            print(f"Channel {self.CHANNEL_NAME} not available for {user.name}, trying next.")
            return self._next_handler.handle_notification(user, notification)
        
        print(f"No further channels to try for {user.name} after {self.CHANNEL_NAME} attempt or unavailability.")
        return False