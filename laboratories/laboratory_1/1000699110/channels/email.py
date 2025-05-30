import random
from log.logger import Logger
from channels.base import NotificationChannel

class EmailChannel(NotificationChannel):
    """
    Email Notification Channel
    This class handles sending notifications via email. It inherits from the NotificationChannel base class.

    Args:
        NotificationChannel (NotificationChannel): Base class for all notification channels.
    """
    def handle(self, user, message, priority):
        success = random.choice([True, False])
        Logger().log(f"Trying Email for {user['name']}: {success}")
        if success:
            return True, f"Email sent to {user['name']}"
        if self.next_channel:
            return self.next_channel.handle(user, message, priority)
        return False, "All channels failed"
