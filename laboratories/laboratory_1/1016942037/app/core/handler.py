import random # simular fallos en el envío de notificaciones
from app.utils.logger import Logger # logger Singleton para registrar los intentos de envío

# Clase que representa un canal de comunicación dentro de la cadena de responsabilidad
class ChannelHandler:
    def __init__(self, channel_name):
        """
        Inicializa el canal con su nombre, sin siguiente canal asignado aún.
        También se instancia el logger para registrar eventos.
        """
        self.channel_name = channel_name        # Nombre del canal (ej: "email", "sms", etc.)
        self.next_handler = None                # Siguiente canal en la cadena (puede ser None)
        self.logger = Logger()                  # Instancia del logger Singleton

    def set_next(self, handler):
        """
        Asigna el siguiente canal en la cadena de responsabilidad.
        Devuelve el handler asignado para permitir encadenamiento fluido.
        """
        self.next_handler = handler
        return handler

    def handle(self, message):
        """
        Intenta enviar el mensaje a través de este canal.
        Si falla (simulado aleatoriamente), pasa al siguiente canal si existe.
        """
        success = random.choice([True, False])  # Simula aleatoriamente si el canal falla o no

        self.logger.log(f"Intentando enviar por {self.channel_name}...")

        if success:
            self.logger.log(f"✅ Enviado por {self.channel_name}")
            return True
        else:
            self.logger.log(f"❌ Falló en {self.channel_name}")
            if self.next_handler:
                return self.next_handler.handle(message)  # Intenta con el siguiente canal
            else:
                self.logger.log("🚫 Todos los canales fallaron")  # No quedan más canales
                return False
