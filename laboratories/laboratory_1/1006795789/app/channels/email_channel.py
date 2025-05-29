# email_channel.py
# Implementa el canal de notificación por correo electrónico (simulado).

from app.channels.base_channel import NotificationChannel
from app.core.logger_singleton import Logger
import random

class EmailChannel(NotificationChannel):
    """
    Canal de notificación que simula el envío por correo electrónico.
    El envío puede fallar aleatoriamente para simular errores reales.
    """
    def send(self, user_name, message):
        """
        Intenta enviar el mensaje por email (simulado).
        Registra el intento y el resultado en el logger.
        :param user_name: Nombre del usuario
        :param message: Mensaje a enviar
        :return: True si tuvo éxito, False si falló
        """
        Logger().log(user_name, "email", message, "attempt")
        success = random.choice([True, False])  # Simula éxito o fallo aleatorio
        Logger().log(user_name, "email", message, "success" if success else "failure")
        return success
