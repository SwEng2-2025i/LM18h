from app.patterns.chain_of_responsibility import NotificationHandler, EmailHandler, SMSHandler, ConsoleHandler

class ChannelHandlerFactory:
    _handler_map = {
        "email": EmailHandler,
        "sms": SMSHandler,
        "console": ConsoleHandler
    }

    @staticmethod
    def create_handler(channel_type: str) -> NotificationHandler:
        handler_class = ChannelHandlerFactory._handler_map.get(channel_type.lower())
        if not handler_class:
            raise ValueError(f"Unsupported channel type: {channel_type}")
        return handler_class()

    @staticmethod
    def get_supported_channels() -> list[str]:
        return list(ChannelHandlerFactory._handler_map.keys())