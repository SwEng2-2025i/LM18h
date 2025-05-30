import random
from app.channels.base import Channel
from app.logger import Logger

class SMSChannel(Channel):
    """
    Canal de envío de notificaciones por mensaje de texto SMS.
    Si falla, delega al siguiente canal de la cadena.
    """

    def send(self, message, user):
        Logger().log(f"Intentando enviar por SMS a {user['name']}")
        success = random.choice([True, False])

        if success:
            Logger().log(f"SMS enviado exitosamente a {user['name']}: {message}")
            return f"Enviado por SMS a {user['name']}"
        elif self.next_channel:
            Logger().log("Fallo SMS, intentando siguiente canal...")
            return self.next_channel.send(message, user)
        else:
            Logger().log("Todos los canales fallaron.")
            return f"No se pudo enviar la notificación a {user['name']}"