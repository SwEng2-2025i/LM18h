class Logger:
    """
    Class that implements Singleton design pattern

    Attributes:
        _instance: Single instance of the Logger class
        logs: List of dictionaries containing all the notification attempts 
    """

    _instance = None

    def __new__(cls):
        """
        Method that creates or return the single instance of Logger

        Returns:
            Logger: The single instance of Logger class
        """

        if cls._instance == None:
            cls._instance = super(Logger, cls).__new__(cls)
            cls._instance.logs = []
        return cls._instance
        
    def log(self, user_name: str, message: str, priority: str, channel: str, status: str):
        """
        Method that logs all the notification attempts

        Args:
            user_name: User name of the receiver
            message: Message content
            priority: Priority level of the message ('low', 'medium' or 'high')
            channel: Channel used to send the notification
            status: Delivery status ('failed' or 'completed')
        """
        self.logs.append(
            {
                "user_name": user_name,
                "message": message,
                "priority": priority,
                "channel": channel,
                "status": status
            })

