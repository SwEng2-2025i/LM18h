import random
from logger import Logger

class Handler:
    """
    Base class for the Chain of Responsabilitry pattern

    Attributes:
        next = Next handler in the chain
    """

    def __init__ (self, next=None):
        """
        Initialization of the handler

        Args:
            next: Next handler in the chain (optional)
        """

        self.next = next

    def handle(self, data: dict, logger: Logger) -> bool:
        """
        Delegates the notification to the next handler in the chain

        Args
            data: Dictionary containing user name, message content and priority level
            logger: Logger instance used to record the notification attempts

        Returns:
            bool: True if the message is sent, False otherwise
        """

        if self.next:
            return self.next.handle(data, logger)
        return False

class smsHandler(Handler):
    """
    Handler for the sms channel
    """

    def handle(self, data: dict, logger: Logger) -> bool:
        """
        Tries to send the notification via sms

        Args:
            data: Dictionary containing user name, message content and priority level
            logger: Logger instance used to record the notification attempts

        Returns:
            bool: True if the message is sent, False otherwise
        """

        if random.choice([True, False]):
            logger.log(data["user_name"], data["message"], data["priority"], "sms", "completed")
            return True
        else:
            logger.log(data["user_name"], data["message"], data["priority"], "sms", "failed")
            return super().handle(data, logger)

class emailHandler(Handler):
    """
    Handler for the email channel
    """

    def handle(self, data: dict, logger: Logger) -> bool:
        """
        Tries to send the notification via email

        Args:
            data: Dictionary containing user name, message content and priority level
            logger: Logger instance used to record the notification attempts

        Returns:
            bool: True if the message is sent, False otherwise
        """

        if random.choice([True, False]):
            logger.log(data["user_name"], data["message"], data["priority"], "email", "completed")
            return True
        else:
            logger.log(data["user_name"], data["message"], data["priority"], "email", "failed")
            return super().handle(data, logger)

class consoleHandler(Handler):
    """
    Handler for the console channel
    """

    def handle(self, data: dict, logger: Logger) -> bool:
        """
        Tries to send the notification via console

        Args:
            data: Dictionary containing user name, message content and priority level
            logger: Logger instance used to record the notification attempts

        Returns:
            bool: True if the message is sent, False otherwise
        """

        if random.choice([True, False]):
            logger.log(data["user_name"], data["message"], data["priority"], "console", "completed")
            return True
        else:
            logger.log(data["user_name"], data["message"], data["priority"], "console", "failed")
            return super().handle(data, logger)
    