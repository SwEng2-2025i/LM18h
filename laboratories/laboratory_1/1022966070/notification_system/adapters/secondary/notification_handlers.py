import logging

from notification_system.domain.models import ChannelType, Notification
from notification_system.domain.ports.notification import NotificationHandler


class ConsoleNotificationHandler(NotificationHandler):
    def handle(self, notification: Notification, user_channels: list) -> Notification:
        logging.info(f"Console Notification for {notification.user_name}: {notification.message}")
        return notification
    
    def can_handle(self, channel) -> bool:
        return channel == ChannelType.CONSOLE

class EmailNotificationHandler(NotificationHandler):
    def handle(self, notification: Notification, user_channels: list) -> Notification:
        logging.info(f"Email Notification for {notification.user_name}: {notification.message}")
        return notification
    
    def can_handle(self, channel) -> bool:
        return channel == ChannelType.EMAIL

class SMSNotificationHandler(NotificationHandler):
    def handle(self, notification: Notification, user_channels: list) -> Notification:
        logging.info(f"SMS Notification for {notification.user_name}: {notification.message}")
        return notification
    
    def can_handle(self, channel) -> bool:
        return channel == ChannelType.SMS