from domain.entities.user import User
from domain.ports.user_ports import UserInputPort, UserOutputPort
from application.factories.user_factory import UserFactory

class UserServices(UserInputPort):
    """
    Implements the user-related application logic.
    Coordinates user registration and retrieval.
    """

    def __init__(self, storage: UserOutputPort, factory: UserFactory):
        self.storage = storage
        self.factory = factory

    def register_user(self, name: str, preferred_channel: str, available_channels: list[str]) -> User:
        """
        Registers a new user if the name is not already taken.

        Raises:
            ValueError: If the user already exists.
        """

        if self.storage.get_by_name(name):
            raise ValueError(f"User '{name}' already exists.")
        
        user = self.factory.create(name, preferred_channel, available_channels)
        self.storage.save_user(user)
        return user

    def list_users(self) -> list[User]:
        """
        Returns all registered users.
        """
        
        return self.storage.list_all()