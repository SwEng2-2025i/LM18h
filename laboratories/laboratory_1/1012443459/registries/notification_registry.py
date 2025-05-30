"""
Notification Registry using Singleton pattern.

Maintains a single instance tracking all sent notifications.
"""

class NotificationRegistry:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(NotificationRegistry, cls).__new__(cls)
            cls._instance._notifications = []
        return cls._instance

    def add_notification(self, notification_data):
        self._notifications.append(notification_data)

    def get_all_notifications(self):
        return self._notifications
