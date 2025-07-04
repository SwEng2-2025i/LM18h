from domain.entities.notification import Notification
from domain.ports.notification_ports import NotificationInputPort, NotificationOutputPort
from domain.ports.user_ports import UserOutputPort
from application.factories.notification_factory import NotificationFactory

class NotificationServices(NotificationInputPort):
    """
    Handles notification-related business logic.
    Responsible for creating and dispatching notifications.
    """

    def __init__(self, user_storage: UserOutputPort, sender: NotificationOutputPort, factory: NotificationFactory):
        self.user_storage = user_storage
        self.sender = sender
        self.factory = factory

    def notify_user(self, user_name: str, message: str, priority: str) -> tuple[Notification, bool]:
        """
        Sends a notification to the specified user.

        Returns:
            - Notification object
            - Success flag (bool)
            - Channel used (or None if all failed)

        Raises:
            ValueError: If the user does not exist.
        """
        
        user = self.user_storage.get_by_name(user_name)

        if not user:
            raise ValueError(f"User '{user_name}' does not exist.")
        
        notification = self.factory.create(user_name = user_name, message = message, priority = priority)

        success, channel_used = self.sender.send_notification(user.available_channels, notification)
        return notification, success, channel_used