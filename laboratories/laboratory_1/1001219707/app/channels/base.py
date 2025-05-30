from abc import ABC, abstractmethod

class Channel(ABC):
    """
    Clase abstracta base para todos los canales de notificación.
    Implementa el patrón Chain of Responsibility.
    """

    def __init__(self):
        self.next_channel = None  # Siguiente canal en la cadena

    def set_next(self, next_channel):
        """
        Define el siguiente canal a intentar en caso de fallo.
        Retorna el mismo canal para permitir el encadenamiento fluido.
        """
        self.next_channel = next_channel
        return next_channel

    @abstractmethod
    def send(self, message, user):
        """
        Método abstracto que debe implementar cada canal.
        Intenta enviar el mensaje al usuario.
        """
        pass