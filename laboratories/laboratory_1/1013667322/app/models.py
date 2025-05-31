"""
Modelos de datos para el sistema de notificaciones
"""
from dataclasses import dataclass
from typing import List


@dataclass
class User:
    """Modelo de usuario con canales de comunicación"""
    name: str
    preferred_channel: str
    available_channels: List[str]
    
    def to_dict(self):
        return {
            'name': self.name,
            'preferred_channel': self.preferred_channel,
            'available_channels': self.available_channels
        }


@dataclass
class Notification:
    """Modelo de notificación"""
    user_name: str
    message: str
    priority: str
    
    def to_dict(self):
        return {
            'user_name': self.user_name,
            'message': self.message,
            'priority': self.priority
        }


@dataclass
class NotificationResult:
    """Resultado de envío de notificación"""
    success: bool
    channel_used: str
    attempts: List[str]
    message: str
    
    def to_dict(self):
        return {
            'success': self.success,
            'channel_used': self.channel_used,
            'attempts': self.attempts,
            'message': self.message
        }
