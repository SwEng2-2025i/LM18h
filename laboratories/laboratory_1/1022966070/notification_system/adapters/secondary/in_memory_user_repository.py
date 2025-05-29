from typing import List, Optional, Dict
from notification_system.domain.models import User
from notification_system.domain.ports.user_repository import UserRepository


class InMemoryUserRepository(UserRepository):
    def __init__(self):
        self._users: Dict[str, User] = {}
    
    def save(self, user: User) -> User:
        self._users[user.name] = user
        return user
    
    def find_by_name(self, name: str) -> Optional[User]:
        return self._users.get(name)
    
    def find_all(self) -> List[User]:
        return list(self._users.values())