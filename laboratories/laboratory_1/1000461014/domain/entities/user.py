from dataclasses import dataclass

@dataclass
class User:
    """
    Represents a system user who can receive notifications through multiple channels.
    
    Attributes:
        name (str): The name of the user.
        preferred_channel (str): The user's preferred notification channel (e.g., 'email').
        available_channels (list[str]): A list of channels the user can receive notifications through.
    """
    
    name: str
    preferred_channel: str
    available_channels: list[str]