"""
User Registry for managing system users.

Maintains in-memory collection of registered users and their preferences.
"""

class UserRegistry:
    def __init__(self):
        self._users = []

    def add_user(self, user_data):
        self._users.append(user_data)
        return user_data

    def get_all_users(self):
        return self._users

    def find_user_by_name(self, name):
        return next((user for user in self._users if user["name"] == name), None)