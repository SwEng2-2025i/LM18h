import random
from models.channels import EmailChannel, SMSChannel, ConsoleChannel

class NotificationService:
    def send(self, notification):
        user = notification.user
        message = notification.message
        
        # Diccionario que relaciona nombres de canal con sus clases correspondientes
        channel_map = {
            'email': EmailChannel,
            'sms': SMSChannel,
            'console': ConsoleChannel
        }
        
        # Se arma la lista de canales, comenzando por el canal preferido del usuario
        channels = [user.preferred_channel] + [ch for ch in user.available_channels if ch != user.preferred_channel]

        attempts = []
        channel_used = None

        # Simula la lógica de la cadena de responsabilidad
        for ch in channels:
            # Se crea una instancia del canal
            channel_instance = channel_map[ch](None)

            # Simula un intento de envío con resultado aleatorio
            success = random.choice([True, False])

            # Registra el intento
            attempts.append({
                'channel': ch,
                'success': success
            })

            # Si el envío fue exitoso, se detiene el proceso
            if success:
                channel_used = ch
                break

        # Devuelve el resultado del intento de notificación
        return {
            'success': channel_used is not None,
            'channel_used': channel_used,
            'attempts': attempts
        }
