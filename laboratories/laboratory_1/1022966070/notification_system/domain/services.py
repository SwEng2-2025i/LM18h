import random
from typing import List
from typing import List, Optional 
from .models import ChannelType, Notification
from .ports.notification import NotificationHandler

class NotificationService:
    def __init__(self, handlers: List[NotificationHandler]):
        self.handlers = handlers
    
    def send_notification(self, notification: Notification, user_channels: List[ChannelType]) -> Notification:
        # Order channels with preferred first
        ordered_channels = self._order_channels(
            user_channels, 
            notification.priority
        )
        
        # Try each channel in order until success
        for channel in ordered_channels:
            handler = self._get_handler_for_channel(channel)
            if handler:
                # Simulate random failure (50% chance)
                if random.choice([True, False]):
                    notification.delivered_via = channel
                    notification.status = "DELIVERED"
                    return handler.handle(notification, user_channels)
                notification.status = f"FAILED ({channel.name})"
        
        notification.status = "FAILED (all channels)"
        return notification
    
    def _order_channels(self, channels: List[ChannelType], priority) -> List[ChannelType]:
        # In a real system, we might prioritize differently based on priority
        return channels
    
    def _get_handler_for_channel(self, channel: ChannelType) -> Optional[NotificationHandler]:
        for handler in self.handlers:
            if handler.can_handle(channel):
                return handler
        return None