# sms_channel.py
# Implementa el canal de notificación por SMS (simulado).

from app.channels.base_channel import NotificationChannel
from app.core.logger_singleton import Logger
import random

class SMSChannel(NotificationChannel):
    """
    Canal de notificación que simula el envío por SMS.
    El envío puede fallar aleatoriamente para simular errores reales.
    """
    def send(self, user_name, message):
        """
        Intenta enviar el mensaje por SMS (simulado).
        Registra el intento y el resultado en el logger.
        :param user_name: Nombre del usuario
        :param message: Mensaje a enviar
        :return: True si tuvo éxito, False si falló
        """
        Logger().log(user_name, "sms", message, "attempt")
        success = random.choice([True, False])  # Simula éxito o fallo aleatorio
        Logger().log(user_name, "sms", message, "success" if success else "failure")
        return success
