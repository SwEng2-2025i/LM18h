from app.channels.base import NotificationChannel
import random

# Clase que representa el canal de notificaciones por SMS.
# Hereda de NotificationChannel y define el comportamiento específico para enviar mensajes por SMS.
class SMSChannel(NotificationChannel):
    def send(self, message, user):
        """
        Envía un mensaje al usuario a través del canal SMS.
        Simula el envío utilizando un resultado aleatorio para determinar si fue exitoso o no.

        Args:
            message (str): El mensaje a enviar.
            user (User): El usuario destinatario del mensaje.

        Returns:
            bool: True si el envío fue exitoso, False en caso contrario.
        """
        print(f"Enviando por SMS a {user.name}...")  # Simula el envío del mensaje
        success = random.choice([True, False])  # Determina aleatoriamente el éxito del envío
        print("Éxito" if success else "Falló")  # Imprime el resultado del envío
        return success  # Retorna el resultado