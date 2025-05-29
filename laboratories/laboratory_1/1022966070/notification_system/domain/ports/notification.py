from abc import ABC, abstractmethod
from ..models import Notification

class NotificationHandler(ABC):
    @abstractmethod
    def handle(self, notification: Notification, user_channels: list) -> Notification:
        pass
    
    @abstractmethod
    def can_handle(self, channel) -> bool:
        pass