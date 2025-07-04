from abc import ABC, abstractmethod
from domain.entities.notification import Notification

class NotificationInputPort(ABC):
    """
    Interface for application-level notification use cases.
    Defines how the application receives notification requests.
    """

    @abstractmethod
    def notify_user(self, user_name: str, message: str, priority: str) -> tuple[Notification, bool]:
        """
        Handle the process of notifying a user.

        Returns:
            A tuple containing the Notification object and a boolean indicating success.
        """
        
        pass 

class NotificationOutputPort(ABC):
    """
    Interface for sending notifications through different channels.
    Defines the communication with the infrastructure layer.
    """

    @abstractmethod
    def send_notification(self, available_channels: list[str], notification: Notification) -> tuple[bool, str | None]:
        """
        Sends the notification via the best available channel.

        Returns:
            A tuple (success, used_channel), where used_channel is None if all failed.
        """
        
        pass