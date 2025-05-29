# console_channel.py
# Implementa el canal de notificación por consola.

from app.channels.base_channel import NotificationChannel
from app.core.logger_singleton import Logger

class ConsoleChannel(NotificationChannel):
    """
    Canal de notificación que simula el envío por consola.
    Este canal nunca falla y siempre entrega el mensaje.
    """
    def send(self, user_name, message):
        """
        Envía el mensaje por consola (simulado).
        Registra el intento y el éxito en el logger.
        :param user_name: Nombre del usuario
        :param message: Mensaje a enviar
        :return: True (siempre tiene éxito)
        """
        Logger().log(user_name, "console", message, "attempt")
        # Console nunca falla
        Logger().log(user_name, "console", message, "success")
        print(f"[Console] {user_name}: {message}")
        return True
