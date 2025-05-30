from app.channels.base import NotificationChannel  
import random                                    

class SMSChannel(NotificationChannel):             # Define el canal SMS heredando de NotificationChannel
    def __init__(self):
        super().__init__()                        # Llama al constructor de la clase base
        self.channel_type = "SMS"                 # Define el tipo de canal como 'SMS'

    def handle(self, user_name, message):
        success = random.choice([True, False])    # Simula si el envío es exitoso o no
        print(f"[SMS] Trying to notify {user_name}... ", end="")  # Muestra intento de notificación
        if success:
            print("✅ Success!")                   # Notificación exitosa
            return True
        else:
            print("❌ Failed.")                    # Notificación fallida
            if self.next_channel:                 # Si hay un canal siguiente, intenta notificar por ese canal
                return self.next_channel.handle(user_name, message)
            return False                          # Si no hay más canales, retorna False