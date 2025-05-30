import random
from log.logger import Logger
from channels.base import NotificationChannel

class SMSChannel(NotificationChannel):
    """
    SMS Notification Channel
    This class handles sending notifications via SMS. It inherits from the NotificationChannel base class.

    Args:
        NotificationChannel (NotificationChannel): Base class for all notification channels.
    """
    def handle(self, user, message, priority):
        success = random.choice([True, False])
        Logger().log(f"Trying SMS for {user['name']}: {success}")
        if success:
            return True, f"SMS sent to {user['name']}"
        if self.next_channel:
            return self.next_channel.handle(user, message, priority)
        return False, "All channels failed"
