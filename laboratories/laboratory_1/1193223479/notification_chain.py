from handlers.email_handler import EmailHandler
from handlers.sms_handler import SMSHandler
from handlers.console_handler import ConsoleHandler
from handlers.phone_call_handler import PhoneCallHandler

# Build chain: Email → SMS → Console → Phone
def build_notification_chain():
    return EmailHandler(
        SMSHandler(
            ConsoleHandler(
                PhoneCallHandler()
            )
        )
    )
