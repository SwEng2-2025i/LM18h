from typing import List, Dict, Any

class User:
    def __init__(self, name: str, preferred_channel: str, available_channels: List[str]):
        if not name:
            raise ValueError("User name cannot be empty.")
        if not preferred_channel:
            raise ValueError("Preferred channel cannot be empty.")
        if not available_channels:
            raise ValueError("Available channels cannot be empty.")
        if preferred_channel not in available_channels:
            raise ValueError(f"Preferred channel '{preferred_channel}' must be one of the available channels: {available_channels}")
        
        self.name = name
        self.preferred_channel = preferred_channel
        self.available_channels = list(set(available_channels)) # Ensure unique channels

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "preferred_channel": self.preferred_channel,
            "available_channels": self.available_channels
        }

class NotificationData:
    def __init__(self, user_name: str, message: str, priority: str):
        if not user_name:
            raise ValueError("User name for notification cannot be empty.")
        if not message:
            raise ValueError("Notification message cannot be empty.")
        
        self.user_name = user_name
        self.message = message
        self.priority = priority if priority else "medium" # Default priority