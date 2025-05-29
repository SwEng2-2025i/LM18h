from app.channels.base import NotificationChannel
from app.logger.logger import LoggerSingleton
import random

# Clase que representa el canal de notificaciones por Email.
# Hereda de NotificationChannel y define el comportamiento específico para enviar mensajes por correo electrónico.
class EmailChannel(NotificationChannel):
    def send(self, message, user):
        """
        Envía un mensaje al usuario a través del canal de Email.
        Simula el envío utilizando un resultado aleatorio para determinar si fue exitoso o no.
        Además, registra el resultado del envío en el LoggerSingleton.

        Args:
            message (str): El mensaje a enviar.
            user (User): El usuario destinatario del mensaje.

        Returns:
            bool: True si el envío fue exitoso, False en caso contrario.
        """
        logger = LoggerSingleton()  # Obtiene la instancia única del logger
        print(f"Enviando por Email a {user.name}...")  # Simula el envío del mensaje
        success = random.choice([True, False])  # Determina aleatoriamente el éxito del envío
        status = "success" if success else "fail"  # Define el estado del envío
        logger.log(user.name, "email", message, status)  # Registra el resultado en el logger
        print("Éxito" if success else "Falló")  # Imprime el resultado del envío
        return success  # Retorna el resultado