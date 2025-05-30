# Almacenamiento en memoria de usuarios
users_db = {}

class UserService:
    def register_user(self, name, preferred_channel, available_channels):
        users_db[name] = {
            "preferred_channel": preferred_channel,
            "available_channels": available_channels
        }

    def get_users(self):
        return users_db

    def get_user(self, name):
        return users_db.get(name)
