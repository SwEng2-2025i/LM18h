from models.user import User

class UserService:
    def __init__(self):
        self.users = {}

    def add_user(self, name, preferred_channel, available_channels):
        self.users[name] = User(name, preferred_channel, available_channels)

    def get_all_users(self):
        return list(self.users.values())

    def get_user(self, name):
        return self.users.get(name, None)
