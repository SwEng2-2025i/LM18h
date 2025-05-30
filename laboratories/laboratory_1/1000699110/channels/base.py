class NotificationChannel:
    """
    Base class for all notification channels.
    Defines the interface for handling notifications and chaining channels.
    """
    def __init__(self, name):
        self.name = name
        self.next_channel = None

    def set_next(self, channel):
        self.next_channel = channel
        return channel

    # Method to handle the notification logic - polymorphic
    def handle(self, user, message, priority):
        raise NotImplementedError