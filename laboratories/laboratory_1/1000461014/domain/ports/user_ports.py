from abc import ABC, abstractmethod
from domain.entities.user import User

class UserInputPort(ABC):
    """
    Interface for user-related application logic.
    Defines the operations that can be performed on users.
    """

    @abstractmethod
    def register_user(self, name: str, preferred_channel: str, available_channels: list[str]) -> User:
        """
        Register a new user in the system.

        Returns:
            The registered User object.
        """
        
        pass

    @abstractmethod
    def list_users(self) -> list[User]:
        """
        Retrieve all registered users.

        Returns:
            A list of User objects.
        """
        
        pass

class UserOutputPort(ABC):
    """
    Interface for persistence operations related to users.
    Allows for storage, retrieval, and lookup.
    """

    @abstractmethod
    def save_user(self, user: User) -> None:
        """
        Persist a new user in memory.
        """

        pass

    @abstractmethod
    def list_all(self) -> list[User]:
        """
        Retrieve all users from the storage.

        Returns:
            A list of User objects.
        """
        
        pass

    @abstractmethod
    def get_by_name(self, name: str) -> User | None:
        """
        Find a user by name.

        Returns:
            The User object if found, otherwise None.
        """
        
        pass

    
