"""
Implementación de los patrones de diseño
"""
from abc import ABC, abstractmethod
from typing import Optional


class Logger:
    """Patrón Singleton - Logger único para toda la aplicación"""
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Logger, cls).__new__(cls)
            cls._instance.logs = []
        return cls._instance
    
    def log(self, message: str):
        """Registra un mensaje en el log"""
        self.logs.append(message)
        print(f"[LOG] {message}")
    
    def get_logs(self):
        """Obtiene todos los logs"""
        return self.logs.copy()


class NotificationHandler(ABC):
    """Clase abstracta para el patrón Chain of Responsibility"""
    def __init__(self):
        self._next_handler: Optional[NotificationHandler] = None
        self.logger = Logger()
    
    def set_next(self, handler: 'NotificationHandler') -> 'NotificationHandler':
        """Establece el siguiente handler en la cadena"""
        self._next_handler = handler
        return handler
    
    @abstractmethod
    def handle(self, channel: str, message: str, user_name: str) -> tuple[bool, str]:
        """Maneja el envío de notificación"""
        pass
        
    def _try_send(self, channel: str, message: str, user_name: str) -> bool:
        """Simula el envío de notificación"""
        success = True  # Siempre exitoso para simplicidad
        status = "SUCCESS" if success else "FAILED"
        self.logger.log(f"Attempt to send via {channel} to {user_name}: {status}")
        return success


class EmailHandler(NotificationHandler):
    """Handler para notificaciones por email"""
    
    def handle(self, channel: str, message: str, user_name: str) -> tuple[bool, str]:
        if channel == "email":
            success = self._try_send("email", message, user_name)
            if success:
                return True, "email"
        
        if self._next_handler:
            return self._next_handler.handle(channel, message, user_name)
        return False, ""


class SMSHandler(NotificationHandler):
    """Handler para notificaciones por SMS"""
    
    def handle(self, channel: str, message: str, user_name: str) -> tuple[bool, str]:
        if channel == "sms":
            success = self._try_send("sms", message, user_name)
            if success:
                return True, "sms"
        
        if self._next_handler:
            return self._next_handler.handle(channel, message, user_name)
        return False, ""


class ConsoleHandler(NotificationHandler):
    """Handler para notificaciones por consola"""
    
    def handle(self, channel: str, message: str, user_name: str) -> tuple[bool, str]:
        if channel == "console":
            success = self._try_send("console", message, user_name)
            if success:
                return True, "console"
        
        if self._next_handler:
            return self._next_handler.handle(channel, message, user_name)
        return False, ""


class NotificationChain:
    """Maneja la cadena de responsabilidad para notificaciones"""
    
    def __init__(self):
        self.logger = Logger()
        
        # Crear handlers
        self.email_handler = EmailHandler()
        self.sms_handler = SMSHandler()
        self.console_handler = ConsoleHandler()
        
        # Configurar cadena
        self.email_handler.set_next(self.sms_handler).set_next(self.console_handler)
    
    def send_notification(self, channels: list, message: str, user_name: str) -> tuple[bool, str, list]:
        """Envía notificación intentando con todos los canales disponibles"""
        attempts = []
        
        for channel in channels:
            attempts.append(channel)
            success, channel_used = self.email_handler.handle(channel, message, user_name)
            if success:
                return True, channel_used, attempts
        
        return False, "", attempts
