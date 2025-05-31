from domain.entities.notification import Notification

class NotificationFactory:
    """
    Factory for creating Notification instances.
    """
    
    def create(self, user_name: str, message: str, priority: str) -> Notification:
        return Notification(user_name, message, priority)
