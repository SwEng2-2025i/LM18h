# base_channel.py
# Define la clase base abstracta para los canales de notificación.
# Implementa el patrón Chain of Responsibility.

import random
from abc import ABC, abstractmethod

class NotificationChannel(ABC):
    """
    Clase base abstracta para los canales de notificación.
    Implementa el patrón Chain of Responsibility, permitiendo encadenar canales.
    """
    def __init__(self):
        self._next = None  # Siguiente canal en la cadena

    def set_next(self, channel):
        """
        Establece el siguiente canal en la cadena.
        :param channel: Instancia del siguiente canal
        :return: El canal agregado (para encadenamiento)
        """
        self._next = channel
        return channel

    def notify(self, user_name, message):
        """
        Intenta enviar la notificación usando este canal.
        Si falla, pasa la notificación al siguiente canal en la cadena.
        :param user_name: Nombre del usuario
        :param message: Mensaje a enviar
        :return: True si se entregó, False si fallaron todos los canales
        """
        if self.send(user_name, message):
            return True
        elif self._next:
            return self._next.notify(user_name, message)
        return False

    @abstractmethod
    def send(self, user_name, message):
        """
        Método abstracto que debe implementar cada canal concreto.
        Debe intentar enviar la notificación y devolver True si tuvo éxito, False si falla.
        """
        pass
