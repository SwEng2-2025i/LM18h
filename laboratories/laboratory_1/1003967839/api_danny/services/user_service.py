from models.user import User

class UserService:
    def __init__(self):
        self.users = []

    def create_user(self, name, preferred_channel, available_channels):
        user = User(name, preferred_channel, available_channels)
        self.users.append(user)
        return user

    def get_user_by_name(self, name):
        for user in self.users:
            if user.name == name:
                return user
        return None

    def get_all_users(self):
        return self.users