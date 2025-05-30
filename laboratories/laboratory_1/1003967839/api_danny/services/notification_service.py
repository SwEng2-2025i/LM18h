from handlers.email_handler import EmailHandler
from handlers.sms_handler import SMSHandler
from handlers.console_handler import ConsoleHandler

class NotificationService:
    def __init__(self):
        # Setup the chain of responsibility
        self.email_handler = EmailHandler()
        self.sms_handler = SMSHandler()
        self.console_handler = ConsoleHandler()
        
        # Build the chain
        self.email_handler.set_next(self.sms_handler).set_next(self.console_handler)

    def send_notification(self, user, message, priority):
        # Try preferred channel first
        if user.preferred_channel == "email":
            return self.email_handler.handle(user, message, priority)
        elif user.preferred_channel == "sms":
            return self.sms_handler.handle(user, message, priority)
        elif user.preferred_channel == "console":
            return self.console_handler.handle(user, message, priority)
        else:
            # Default to email first if preferred channel is invalid
            return self.email_handler.handle(user, message, priority)