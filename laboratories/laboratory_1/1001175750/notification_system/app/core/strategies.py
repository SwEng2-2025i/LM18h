import random

# Strategy pattern is used to select the sending method dynamically

class NotificationStrategy:
    def send(self, message):
        """
        Base method for sending a notification.
        Must be implemented by all concrete strategies.
        
        :param message: str - The message to send.
        :raises NotImplementedError: if not implemented by subclass.
        """
        raise NotImplementedError("Each strategy must implement the send method.")

class EmailNotification(NotificationStrategy):
    def send(self, message):
        """
        Concrete strategy for sending an email notification.
        
        :param message: str - The message to send.
        :return: bool - Simulates success or failure randomly.
        """
        print(f" Email: {message}")
        return random.choice([True, False])

class SMSNotification(NotificationStrategy):
    def send(self, message):
        """
        Concrete strategy for sending an SMS notification.
        
        :param message: str - The message to send.
        :return: bool - Simulates success or failure randomly.
        """
        print(f" SMS: {message}")
        return random.choice([True, False])

class ConsoleNotification(NotificationStrategy):
    def send(self, message):
        """
        Concrete strategy for sending a notification to the console.
        
        :param message: str - The message to send.
        :return: bool - Simulates success or failure randomly.
        """
        print(f" Console: {message}")
        return random.choice([True, False])

class NotificationContext:
    def __init__(self, strategy: NotificationStrategy):
        """
        Context class that holds a reference to a strategy instance.
        
        :param strategy: NotificationStrategy - The strategy to use.
        """
        self.strategy = strategy

    def execute(self, message):
        """
        Executes the send method of the current strategy.
        
        :param message: str - The message to send.
        :return: bool - The result of the send operation.
        """
        return self.strategy.send(message)

def get_strategy(channel_name):
    """
    Factory method to get the proper NotificationContext based on channel name.
    
    :param channel_name: str - The name of the channel ('email', 'sms', 'console').
    :return: NotificationContext - Context with the correct strategy.
    :raises ValueError: If the channel name is unknown.
    """
    strategies = {
        "email": EmailNotification,
        "sms": SMSNotification,
        "console": ConsoleNotification
    }
    StrategyClass = strategies.get(channel_name)
    if not StrategyClass:
        raise ValueError(f"Unknown channel: {channel_name}")
    return NotificationContext(StrategyClass())
