import uuid
from datetime import datetime
from typing import Optional

class Notification:
    """Notification model representing a message to be sent"""
    
    def __init__(self, user_name: str, message: str, priority: str):
        self.id = str(uuid.uuid4())
        self.user_name = user_name
        self.message = message
        self.priority = priority
        self.timestamp = datetime.now()
        self.delivery_status = "pending"
        self.delivery_channel = None
        self.attempts = []
    
    def add_attempt(self, channel: str, success: bool, error_message: Optional[str] = None):
        """Record a delivery attempt"""
        attempt = {
            'channel': channel,
            'success': success,
            'timestamp': datetime.now(),
            'error_message': error_message
        }
        self.attempts.append(attempt)
        
        if success:
            self.delivery_status = "delivered"
            self.delivery_channel = channel
    
    def mark_failed(self):
        """Mark notification as failed after all attempts"""
        self.delivery_status = "failed"
    
    def __repr__(self):
        return f"Notification(id='{self.id}', user='{self.user_name}', priority='{self.priority}', status='{self.delivery_status}')"
