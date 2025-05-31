from models.user import User

class UserService:
    def __init__(self):
        self.users = {}

    def register_user(self, name, preferred_channel, available_channels):
        if name in self.users:
            raise ValueError(f"User {name} already exists")
        
        if preferred_channel not in available_channels:
            raise ValueError(f"Preferred channel {preferred_channel} must be in available channels")
        
        user = User(name, preferred_channel, available_channels)
        self.users[name] = user
        return user

    def get_user(self, name):
        return self.users.get(name)

    def get_all_users(self):
        return list(self.users.values()) 