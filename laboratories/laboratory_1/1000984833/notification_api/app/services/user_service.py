# app/services/user_service.py

from app.models.user_model import User

# Almacén en memoria
users = []

def add_user(name, preferred_channel, available_channels):
    user = User(name, preferred_channel, available_channels)
    users.append(user)
    return user

def get_all_users():
    return [user.to_dict() for user in users]
