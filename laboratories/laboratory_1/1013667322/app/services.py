"""
Servicios de lógica de negocio
"""
from typing import List, Optional
from app.models import User, Notification, NotificationResult
from app.patterns import NotificationChain, Logger


class UserService:
    """Servicio para gestión de usuarios"""
    
    def __init__(self):
        self.users = {}  # Almacenamiento en memoria
        self.logger = Logger()
    
    def register_user(self, name: str, preferred_channel: str, available_channels: List[str]) -> User:
        """Registra un nuevo usuario"""
        if name in self.users:
            raise ValueError(f"User {name} already exists")
        
        # Validar canales
        valid_channels = ["email", "sms", "console"]
        if preferred_channel not in valid_channels:
            raise ValueError(f"Invalid preferred channel: {preferred_channel}")
        
        for channel in available_channels:
            if channel not in valid_channels:
                raise ValueError(f"Invalid channel: {channel}")
        
        if preferred_channel not in available_channels:
            raise ValueError("Preferred channel must be in available channels")
        
        user = User(name, preferred_channel, available_channels)
        self.users[name] = user
        self.logger.log(f"User registered: {name}")
        return user
    
    def get_user(self, name: str) -> Optional[User]:
        """Obtiene un usuario por nombre"""
        return self.users.get(name)
    
    def get_all_users(self) -> List[User]:
        """Obtiene todos los usuarios"""
        return list(self.users.values())


class NotificationService:
    """Servicio para envío de notificaciones"""
    
    def __init__(self):
        self.notification_chain = NotificationChain()
        self.logger = Logger()
    
    def send_notification(self, user: User, notification: Notification) -> NotificationResult:
        """Envía una notificación a un usuario"""
        self.logger.log(f"Sending notification to {user.name}: {notification.message}")
        
        # Organizar canales: preferido primero, luego el resto
        channels = [user.preferred_channel]
        for channel in user.available_channels:
            if channel != user.preferred_channel:
                channels.append(channel)
        
        # Intentar envío
        success, channel_used, attempts = self.notification_chain.send_notification(
            channels, notification.message, user.name
        )
        
        if success:
            message = f"Notification sent successfully via {channel_used}"
        else:
            message = "Failed to send notification through all available channels"
        
        self.logger.log(message)
        
        return NotificationResult(
            success=success,
            channel_used=channel_used,
            attempts=attempts,
            message=message
        )
