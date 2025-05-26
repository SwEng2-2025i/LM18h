import random
from app.models.logger import Logger

# Clase base para los canales de notificación (parte del patrón Chain of Responsibility)
class Channel:
    def __init__(self, successor=None):
        self.successor = successor # Canal al que se delega si falla el actual

    def send(self, message):
        raise NotImplementedError # Método que debe implementarse en las subclases

# Canal de notificación por correo electrónico
class EmailChannel(Channel):
    def send(self, message):
        logger = Logger()
        if random.choice([True, False]): # Simula éxito o falla aleatoria
            logger.log(f"Email sent: {message}")
            return True
        logger.log("Email failed. Trying next channel.")
        # Intenta el siguiente canal si existe
        return self.successor.send(message) if self.successor else False

# Canal de notificación por SMS
class SMSChannel(Channel):
    def send(self, message):
        logger = Logger()
        if random.choice([True, False]):
            logger.log(f"SMS sent: {message}")
            return True
        logger.log("SMS failed. Trying next channel.")
        return self.successor.send(message) if self.successor else False

# Canal de salida por consola (último recurso)
class ConsoleChannel(Channel):
    def send(self, message):
        logger = Logger()
        if random.choice([True, False]):
            logger.log(f"Console output: {message}")
            return True
        logger.log("Console failed. No more channels.") # Fin de la cadena
        return False