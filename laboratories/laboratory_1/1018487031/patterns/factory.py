from patterns.chain_of_responsibility import EmailHandler, SMSHandler, ConsoleHandler
from utils.logger import Logger

class NotificationChannelFactory:
    """Factory Pattern for creating notification channel handlers"""
    
    def __init__(self):
        self.logger = Logger()
    
    def create_channel_handler(self, channel_type: str):
        """Create a notification handler based on channel type"""
        self.logger.log(f"Creating handler for channel: {channel_type}")
        
        if channel_type.lower() == 'email':
            return EmailHandler()
        elif channel_type.lower() == 'sms':
            return SMSHandler()
        elif channel_type.lower() == 'console':
            return ConsoleHandler()
        else:
            self.logger.log(f"❌ Unknown channel type: {channel_type}")
            return None
    
    def get_available_channels(self):
        """Get list of available channel types"""
        return ['email', 'sms', 'console']
