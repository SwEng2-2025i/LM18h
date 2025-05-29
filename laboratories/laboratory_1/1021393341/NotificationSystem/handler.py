from loggerSingleton import Logger

class Handler:
    def __init__(self, nextHandler=None):
        self.next = nextHandler

    # Create a chain
    def setnext(self, nextHandler):
        self.next = nextHandler

    def handle(self, available_channels, message, priority, failures, user_name):
        if self.next:
            self.next.handle(available_channels, message, priority, failures, user_name)

# email channel
class emailExist(Handler):
    def handle(self, available_channels, message, priority, failures, user_name):
        name = "email"
        logger = Logger()
        if name in available_channels and not failures.get(name, True):
            print(f"Sent via EMAIL: {message}")
            logger.log(user_name, name, "success", message)
        else:
            print(f"Failed on EMAIL")
            logger.log(user_name, name, "failure", message)
            super().handle(available_channels, message, priority, failures, user_name)

# SMS channel
class SMSExist(Handler):
    def handle(self, available_channels, message, priority, failures, user_name):
        name = "SMS"
        logger = Logger()
        if name in available_channels and not failures.get(name, True):
            print(f"Sent via SMS: {message}")
            logger.log(user_name, name, "success", message)
        else:
            print(f"Failed on SMS")
            logger.log(user_name, name, "failure", message)
            super().handle(available_channels, message, priority, failures, user_name)

# console channel
class consoleExist(Handler):
    def handle(self, available_channels, message, priority, failures, user_name):
        name = "console"
        logger = Logger()
        if name in available_channels and not failures.get(name, True):
            print(f"Sent via CONSOLE: {message}")
            logger.log(user_name, name, "success", message)
        else:
            print(f"Failed on CONSOLE")
            logger.log(user_name, name, "failure", message)
            super().handle(available_channels, message, priority, failures, user_name)
