from app.channels.base import NotificationChannel
import random

class EmailChannel(NotificationChannel):
    def __init__(self):
        super().__init__()
        # Identificador para este canal de notificación (Email)
        self.channel_type = "Email"
        
    def handle(self, user_name, message):
        # Simula aleatoriamente si el envío del email fue exitoso o fallido
        success = random.choice([True, False])
        print(f"[Email] Trying to notify {user_name}... ", end="")

        if success:
            # Si fue exitoso, confirma la notificación y termina la cadena
            print("✅ Success!")
            return True
        else:
            # Si falla, intenta pasar la notificación al siguiente canal en la cadena
            print("❌ Failed.")
            if self.next_channel:
                return self.next_channel.handle(user_name, message)
            # Retorna False si no hay más canales y no se pudo notificar
            return False
