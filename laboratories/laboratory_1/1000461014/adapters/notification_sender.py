import random
from domain.ports.notification_ports import NotificationOutputPort
from domain.entities.notification import Notification
from adapters.notification_logger import NotificationLogger

#Base handler implementing the Chain of Responsibility
class ChannelHandler:
    def __init__(self, next_handler: 'ChannelHandler' = None):
        self.next_handler = next_handler

    def handle(self,  notification: Notification) -> tuple[bool, str | None]:
        if self.next_handler:
            return self.next_handler.handle(notification)
        return False, None

class EmailHandler(ChannelHandler):
    def handle(self, notification: Notification) -> tuple[bool, str | None]:
        print(f"[INFO] Attempting EMAIL delivery: '{notification.message}")
        success = random.choice([True, False])
        NotificationLogger().log_attempt("email", notification, success)

        if success:
            print("[SUCCESS] EMAIL delivered to '{notification.user_name}")
            return True, "email"
        
        print("[FAILURE] EMAIL delivery failed for '{notification.user_name}")
        return super().handle(notification)

class SMSHandler(ChannelHandler):
    def handle(self, notification: Notification) -> tuple[bool, str | None]:
        print(f"[INFO] Attempting SMS delivery: '{notification.message}")
        success = random.choice([True, False])
        NotificationLogger().log_attempt("sms", notification, success)

        if success:
            print("[SUCCESS] SMS delivered to '{notification.user_name}")
            return True, "sms"
        
        print("[FAILURE] SMS delivery failed for '{notification.user_name}")
        return super().handle(notification)
        
class ConsoleHandler(ChannelHandler):
    def handle(self, notification: Notification) -> tuple[bool, str | None]:
        print(f"[INFO] Attempting CONSOLE delivery: '{notification.message}")
        success = random.choice([True, False])
        NotificationLogger().log_attempt("console", notification, success)

        if success:
            print("[SUCCESS] CONSOLE message delivered to '{notification.user_name}")
            return True, "console"
        
        print("[FAILURE] CONSOLE delivery failed for '{notification.user_name}")
        return super().handle(notification)

CHANNEL_HANDLER_MAP = {
    "email": EmailHandler,
    "sms": SMSHandler,
    "console": ConsoleHandler,
}

#Concrete implementation of NotificationOutputPort using handlers
class NotificationSender(NotificationOutputPort):
    def send_notification(self, available_channels: list[str], notification: Notification) -> tuple[bool, str | None]:
        handler = None
        valid_channels = []

        #Create chain of handlers in reverse priority
        for channel in reversed(available_channels):
            handler_class = CHANNEL_HANDLER_MAP.get(channel)
            
            if handler_class:
                handler = handler_class(handler)
                valid_channels.append(channel)
            else:
                print(f"[WARNING] Unknown channel: {channel}")
            
        if not valid_channels:
            print("[ERROR] No valid channels were configured. Notification not sent.")
            return False, None

        #Start the chain of delivery attempts
        success, used_channel = handler.handle(notification)

        #Log result of delivery
        NotificationLogger().log_delivery_result(notification, used_channel)

        if not success:
            print("[ERROR] All delivery attempts failed.")
        
        return success, used_channel