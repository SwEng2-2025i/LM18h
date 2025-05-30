from .user_service import UserService
from .notification_service import NotificationService

# Crear instancias para exportar
user_service = UserService()
notification_service = NotificationService()

__all__ = ['user_service', 'notification_service']