from app.core.strategies import get_strategy

# Chain of Responsibility pattern is used to chain the handling of sending notifications through different channels.
# If one channel fails to send the notification, the responsibility is passed to the next channel in the chain.

class ChannelHandler:
    def __init__(self, channel):
        """
        Initialize a ChannelHandler for a specific notification channel.

        :param channel: str - The name of the notification channel (e.g., 'email', 'sms', 'console').
        """
        self.channel = channel
        self.next_handler = None

    def set_next(self, handler):
        """
        Set the next handler in the chain.

        :param handler: ChannelHandler - The next handler to delegate to if the current handler fails.
        :return: The handler passed in, to allow chaining.
        """
        self.next_handler = handler
        return handler

    def handle(self, message):
        """
        Attempt to send the message via the current channel.
        If sending fails, pass the responsibility to the next handler in the chain.

        :param message: str - The notification message to send.
        :return: bool - True if the message was successfully sent; False otherwise.
        """

        print(f" Trying channel: {self.channel}")

        # Get the strategy (sending logic) for this channel
        context = get_strategy(self.channel)

        # Execute the sending operation using the strategy
        success = context.execute(message)

        if success:
            print(f" Delivered via {self.channel}")
            return True # Message sent successfull
        else:
            print(f" Failed via {self.channel}")
            if self.next_handler:
                # Delegate to the next handler in the chain
                return self.next_handler.handle(message)
            else:
                # No more handlers available, all channels failed
                print(" All channels failed.")
                return False
