from domain.ports.user_ports import UserOutputPort
from domain.entities.user import User

class InMemoryUserStorage(UserOutputPort):
    """
    Simple in-memory implementation of UserOutputPort.
    """

    def __init__(self):
        self.users = []

    def save_user(self, user: User) -> None:
        self.users.append(user)

    def list_all(self) -> list[User]:
        return self.users
    
    def get_by_name(self, name: str) -> User | None:
        return next((u for u in self.users if u.name == name), None)