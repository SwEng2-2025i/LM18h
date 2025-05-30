from channels.email import EmailChannel
from channels.sms import SMSChannel
from channels.console import ConsoleChannel

class ChannelFactory:
    @staticmethod
    def create(name):
        if name == 'email': return EmailChannel('email')
        if name == 'sms': return SMSChannel('sms')
        if name == 'console': return ConsoleChannel('console')
        raise ValueError(f"Unknown channel: {name}")
