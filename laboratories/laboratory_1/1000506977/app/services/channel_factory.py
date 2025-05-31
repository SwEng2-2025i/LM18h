from .channels import EmailChannel, SMSChannel, ConsoleChannel

class ChannelFactory:
    @staticmethod
    def get_channel(name: str):
        channels = {
            "email": EmailChannel,
            "sms": SMSChannel,
            "console": ConsoleChannel
        }
        channel_cls = channels.get(name.lower())
        if channel_cls:
            return channel_cls()
        raise ValueError(f"Unknown channel: {name}")
