from dataclasses import dataclass
from typing import List
from ..domain.models import User, Notification, ChannelType, NotificationPriority

@dataclass
class UserDTO:
    name: str
    preferred_channel: str
    available_channels: List[str]
    
    @classmethod
    def from_domain(cls, user):
        return cls(
            name=user.name,
            preferred_channel=user.preferred_channel.name,
            available_channels=[ch.name for ch in user.available_channels]
        )
    
    def to_dict(self):
        return {
            'name': self.name,
            'preferred_channel': self.preferred_channel,
            'available_channels': self.available_channels
        }

@dataclass
class NotificationDTO:
    user_name: str
    message: str
    priority: str
    status: str
    delivered_via: str
    
    @classmethod
    def from_domain(cls, notification):
        return cls(
            user_name=notification.user_name,
            message=notification.message,
            priority=notification.priority.name.lower(),
            status=notification.status,
            delivered_via=notification.delivered_via.name if notification.delivered_via else None
        )
    
    def to_dict(self):
        return {
            'user_name': self.user_name,
            'message': self.message,
            'priority': self.priority,
            'status': self.status,
            'delivered_via': self.delivered_via
        }