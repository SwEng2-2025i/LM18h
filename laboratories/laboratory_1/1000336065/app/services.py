from typing import List, Dict, Any
from app.models import User, NotificationData
from app.patterns.factory import ChannelHandlerFactory
from app.patterns.chain_of_responsibility import NotificationHandler
from app.errors import UserNotFoundError, InvalidUsageError

# In-memory storage
users_db: Dict[str, User] = {}

class UserService:
    def register_user(self, name: str, preferred_channel: str, available_channels: List[str]) -> User:
        if name in users_db:
            raise InvalidUsageError(f"User '{name}' already exists.")
        
        supported_channels = ChannelHandlerFactory.get_supported_channels()
        for ch in [preferred_channel] + available_channels:
            if ch not in supported_channels:
                raise InvalidUsageError(f"Channel '{ch}' is not supported. Supported channels are: {supported_channels}")

        user = User(name, preferred_channel, available_channels)
        users_db[user.name] = user
        return user

    def get_all_users(self) -> List[Dict[str, Any]]:
        return [user.to_dict() for user in users_db.values()]

    def get_user_by_name(self, name: str) -> User:
        user = users_db.get(name)
        if not user:
            raise UserNotFoundError(f"User '{name}' not found.")
        return user

class NotificationService:
    def __init__(self):
        self.factory = ChannelHandlerFactory()

    def send_notification(self, user_name: str, message: str, priority: str) -> Dict[str, Any]:
        user = users_db.get(user_name)
        if not user:
            raise UserNotFoundError(f"User '{user_name}' not found to send notification.")

        notification_data = NotificationData(user_name, message, priority)
        
        # Build the chain of responsibility
        # 1. Preferred channel
        # 2. Other available channels (excluding preferred if already added)
        
        chain_head: NotificationHandler = None
        current_handler: NotificationHandler = None
        
        # Add preferred channel first
        try:
            preferred_handler = self.factory.create_handler(user.preferred_channel)
            chain_head = preferred_handler
            current_handler = preferred_handler
        except ValueError as e: # Should not happen if user creation validates channels
            print(f"Warning: Preferred channel {user.preferred_channel} for user {user.name} is invalid: {e}")
            # Potentially log this as a system issue

        # Add other available channels, ensuring no duplicates and preferred is not re-added if it was the first
        other_channels = [ch for ch in user.available_channels if ch != user.preferred_channel]
        
        for channel_type in other_channels:
            try:
                handler = self.factory.create_handler(channel_type)
                if current_handler:
                    current_handler.set_next(handler)
                    current_handler = handler
                else: # This means preferred channel was invalid or not set up
                    chain_head = handler
                    current_handler = handler
            except ValueError as e:
                print(f"Warning: Available channel {channel_type} for user {user.name} is invalid: {e}")

        if not chain_head:
            return {
                "user_name": user_name,
                "message": "Notification not sent. No valid channels configured for user or system.",
                "status": "FAILED_NO_CHANNELS"
            }

        # Attempt to send through the chain
        success = chain_head.handle_notification(user, notification_data)

        return {
            "user_name": user_name,
            "message_sent": notification_data.message,
            "status": "DELIVERED" if success else "DELIVERY_ATTEMPTED_FAILED_ALL_CHANNELS"
        }