# adapters/logger.py
from domain.entities.notification import Notification
from datetime import datetime
class NotificationLogger:
    """
    Singleton logger to track notification delivery attempts and results.
    """

    instance = None

    def __new__(cls):
        if cls.instance is None:
            cls.instance = super(NotificationLogger, cls).__new__(cls)
            cls.instance.logs = []
        return cls.instance

    def log_attempt(self, channel: str, notification: Notification, success: bool):
        #Record and print a delivery attempt
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        entry = {
            "timestamp": timestamp,
            "channel": channel,
            "user": notification.user_name,
            "message": notification.message,
            "priority": notification.priority,
            "success": success
        }
        self.logs.append(entry)

        status = "SUCCESS" if success else "FAILED"
        print(
            f"[{timestamp}] {status} | User: {notification.user_name} | "
            f"Channel: {channel.upper()} | Priority: {notification.priority} | Message: {notification.message}"
        )

    def log_delivery_result(self, notification: Notification, channel_used: str | None):
        #Print the final result of a notification attempt
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if channel_used:
            print(
                f"[{timestamp}] FINAL RESULT | Notification to '{notification.user_name}' delivered via {channel_used.upper()}"
            )
        else:
            print(
                f"[{timestamp}] FINAL RESULT | Notification to '{notification.user_name}' failed on all channels."
            )

        
    def get_logs(self):
        return self.logs
