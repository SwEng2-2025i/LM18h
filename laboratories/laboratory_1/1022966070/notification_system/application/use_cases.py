from typing import List
from ..domain.models import User, Notification
from ..domain.ports.user_repository import UserRepository
from ..domain.services import NotificationService
from ..domain.models import ChannelType, NotificationPriority 

class UserUseCases:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository
    
    def register_user(self, name: str, preferred_channel: str, available_channels: List[str]) -> User:
        
        pref_channel_enum = ChannelType[preferred_channel.upper()]
        avail_channels_enum = [ChannelType[ch.upper()] for ch in available_channels]
        
        user = User(name=name, preferred_channel=pref_channel_enum, available_channels=avail_channels_enum)
        return self.user_repository.save(user)
    
    def list_users(self) -> List[User]:
        return self.user_repository.find_all()

class NotificationUseCases:
    def __init__(self, user_repository: UserRepository, notification_service: NotificationService):
        self.user_repository = user_repository
        self.notification_service = notification_service
    
    def send_notification(self, user_name: str, message: str, priority: str) -> Notification:
        user = self.user_repository.find_by_name(user_name)
        if not user:
            raise ValueError(f"User {user_name} not found")
        
        priority_enum = NotificationPriority[priority.upper()]
        notification = Notification(
            user_name=user_name,
            message=message,
            priority=priority_enum
        )
        
        return self.notification_service.send_notification(notification, user.available_channels)