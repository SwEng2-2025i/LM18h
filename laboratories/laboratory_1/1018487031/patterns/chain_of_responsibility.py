from abc import ABC, abstractmethod
from typing import Optional
import random
from models.notification import Notification
from models.user import User
from utils.logger import Logger

class NotificationHandler(ABC):
    """Abstract base class for notification handlers (Chain of Responsibility Pattern)"""
    
    def __init__(self):
        self._next_handler: Optional[NotificationHandler] = None
        self.logger = Logger()
    
    def set_next(self, handler: 'NotificationHandler') -> 'NotificationHandler':
        """Set the next handler in the chain"""
        self._next_handler = handler
        return handler
    
    @abstractmethod
    def handle(self, notification: Notification) -> dict:
        """Handle the notification or pass to next handler"""
        if self._next_handler:
            return self._next_handler.handle(notification)
        return {
            'success': False,
            'message': 'All notification channels failed',
            'channel': None
        }

class EmailHandler(NotificationHandler):
    """Email notification handler"""
    
    def handle(self, notification: Notification) -> dict:
        self.logger.log(f"Attempting email delivery for notification {notification.id}")
        
        # Simulate random failure
        success = random.choice([True, False])
        
        if success:
            notification.add_attempt('email', True)
            self.logger.log(f"✅ Email delivered successfully for notification {notification.id}")
            return {
                'success': True,
                'message': 'Notification delivered via email',
                'channel': 'email'
            }
        else:
            error_msg = "Email server temporarily unavailable"
            notification.add_attempt('email', False, error_msg)
            self.logger.log(f"❌ Email delivery failed for notification {notification.id}: {error_msg}")
            
            # Try next handler
            return super().handle(notification)

class SMSHandler(NotificationHandler):
    """SMS notification handler"""
    
    def handle(self, notification: Notification) -> dict:
        self.logger.log(f"Attempting SMS delivery for notification {notification.id}")
        
        # Simulate random failure
        success = random.choice([True, False])
        
        if success:
            notification.add_attempt('sms', True)
            self.logger.log(f"✅ SMS delivered successfully for notification {notification.id}")
            return {
                'success': True,
                'message': 'Notification delivered via SMS',
                'channel': 'sms'
            }
        else:
            error_msg = "SMS gateway timeout"
            notification.add_attempt('sms', False, error_msg)
            self.logger.log(f"❌ SMS delivery failed for notification {notification.id}: {error_msg}")
            
            # Try next handler
            return super().handle(notification)

class ConsoleHandler(NotificationHandler):
    """Console notification handler (always succeeds)"""
    
    def handle(self, notification: Notification) -> dict:
        self.logger.log(f"Attempting console delivery for notification {notification.id}")
        
        # Console delivery always succeeds
        notification.add_attempt('console', True)
        self.logger.log(f"✅ Console notification delivered for notification {notification.id}")
        print(f"📱 CONSOLE NOTIFICATION: {notification.message} (Priority: {notification.priority})")
        
        return {
            'success': True,
            'message': 'Notification delivered via console',
            'channel': 'console'
        }

class NotificationChain:
    """Manages the chain of responsibility for notification delivery"""
    
    def __init__(self):
        self.logger = Logger()
    
    def setup_chain(self, user: User, channel_factory):
        """Setup the notification chain based on user preferences"""
        self.logger.log(f"Setting up notification chain for user: {user.name}")
        
        # Create handlers for available channels
        handlers = []
        for channel in user.available_channels:
            handler = channel_factory.create_channel_handler(channel)
            if handler:
                handlers.append(handler)
        
        # Reorder to put preferred channel first
        if user.preferred_channel in user.available_channels:
            preferred_handler = channel_factory.create_channel_handler(user.preferred_channel)
            if preferred_handler:
                # Remove preferred from list if it exists
                handlers = [h for h in handlers if type(h).__name__.lower().replace('handler', '') != user.preferred_channel]
                handlers.insert(0, preferred_handler)
        
        # Chain the handlers
        self.chain_root = None
        if handlers:
            self.chain_root = handlers[0]
            for i in range(len(handlers) - 1):
                handlers[i].set_next(handlers[i + 1])
    
    def send_notification(self, notification: Notification) -> dict:
        """Send notification through the chain"""
        if not self.chain_root:
            notification.mark_failed()
            return {
                'success': False,
                'message': 'No notification channels available',
                'channel': None
            }
        
        self.logger.log(f"Starting notification delivery for {notification.id}")
        result = self.chain_root.handle(notification)
        
        if not result['success']:
            notification.mark_failed()
            self.logger.log(f"❌ All notification channels failed for {notification.id}")
        
        return result
