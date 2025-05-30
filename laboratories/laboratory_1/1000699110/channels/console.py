from log.logger import Logger
from channels.base import NotificationChannel

class ConsoleChannel(NotificationChannel):
    """
    Console Notification Channel
    This class handles sending notifications to the console. It inherits from the NotificationChannel base class.
    
    Args:
        NotificationChannel (NotificationChannel): Base class for all notification channels.
    """
    def handle(self, user, message, priority):
        Logger().log(f"Console output for {user['name']}: {message} (priority {priority})")
        return True, f"Console notified for {user['name']}"
