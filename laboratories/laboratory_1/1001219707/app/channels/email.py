import random
from app.channels.base import Channel
from app.logger import Logger

class EmailChannel(Channel):
    """
    Canal de envío de notificaciones por correo electrónico.
    Si falla, delega al siguiente canal de la cadena.
    """

    def send(self, message, user):
        Logger().log(f"Intentando enviar por EMAIL a {user['name']}")
        success = random.choice([True, False])

        if success:
            Logger().log(f"EMAIL enviado exitosamente a {user['name']}: {message}")
            return f"Enviado por EMAIL a {user['name']}"
        elif self.next_channel:
            Logger().log("Fallo EMAIL, intentando siguiente canal...")
            return self.next_channel.send(message, user)
        else:
            Logger().log("Todos los canales fallaron.")
            return f"No se pudo enviar la notificación a {user['name']}"