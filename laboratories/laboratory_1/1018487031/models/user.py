from typing import List, Optional

class User:
    """User model representing a system user with notification preferences"""
    
    def __init__(self, name: str, preferred_channel: str, available_channels: List[str]):
        self.name = name
        self.preferred_channel = preferred_channel
        self.available_channels = available_channels
    
    def __repr__(self):
        return f"User(name='{self.name}', preferred='{self.preferred_channel}', available={self.available_channels})"

class UserManager:
    """Manages user storage and retrieval (Singleton-like behavior)"""
    
    def __init__(self):
        self._users = {}
    
    def add_user(self, user: User) -> None:
        """Add a user to the system"""
        self._users[user.name] = user
    
    def get_user(self, name: str) -> Optional[User]:
        """Retrieve a user by name"""
        return self._users.get(name)
    
    def get_all_users(self) -> List[User]:
        """Get all registered users"""
        return list(self._users.values())
    
    def remove_user(self, name: str) -> bool:
        """Remove a user from the system"""
        if name in self._users:
            del self._users[name]
            return True
        return False
