from dataclasses import dataclass

@dataclass
class Notification:
    """
    Represents a notification to be sent to a user.
    
    Attributes:
        user_name (str): The recipient user's name.
        message (str): The content of the notification.
        priority (str): The urgency level of the notification (e.g., 'High', 'Low').
    """
    
    user_name: str
    message: str
    priority: str