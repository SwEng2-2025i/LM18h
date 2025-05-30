import random
from app.channels.base import Channel
from app.logger import Logger

class ConsoleChannel(Channel):
    """
    Canal de notificación que imprime en la consola del sistema.
    Se usa como último recurso. También puede fallar aleatoriamente.
    """

    def send(self, message, user):
        Logger().log(f"Intentando enviar por CONSOLE a {user['name']}")
        success = random.choice([True, False])

        if success:
            Logger().log(f"CONSOLE: Notificación para {user['name']} -> {message}")
            return f"Enviado por CONSOLE a {user['name']}"
        elif self.next_channel:
            Logger().log("Fallo CONSOLE, intentando siguiente canal...")
            return self.next_channel.send(message, user)
        else:
            Logger().log("Todos los canales fallaron.")
            return f"No se pudo enviar la notificación a {user['name']}"