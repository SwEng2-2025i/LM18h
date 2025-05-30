from app.channels.base import NotificationChannel
import random

class ConsoleChannel(NotificationChannel):
    def __init__(self):
        super().__init__()
        # Tipo identificador para el canal de notificación
        self.channel_type = "Console"

    def handle(self, user_name, message):
        # Simula aleatoriamente si la notificación es exitosa o falla
        success = random.choice([True, False])
        print(f"[Console] Trying to notify {user_name}... ", end="")

        if success:
            # Notificación exitosa, retorna True para indicar que no sigue la cadena
            print("✅ Success!")
            return True
        else:
            # Notificación fallida, intenta pasar la responsabilidad al siguiente canal
            print("❌ Failed.")
            if self.next_channel:
                return self.next_channel.handle(user_name, message)
            # Si no hay siguiente canal, retorna False indicando que no se pudo notificar
            return False
