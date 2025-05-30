from app.channels.factory import create_channel
from app.utils.logger import Logger

# Instancia única del logger (implementado como Singleton)
logger = Logger()

class NotifierService:
    def __init__(self, logger=logger):
        # Servicio responsable de gestionar el envío de notificaciones.
        # Recibe un logger para registrar los intentos de envío.
        self.logger = logger

    def send_notification(self, user, message):
        # Obtiene la lista de canales disponibles para el usuario
        channels = user.available_channels

        # Reordena los canales para que el canal preferido sea el primero
        ordered_channels = [user.preferred_channel] + [ch for ch in channels if ch != user.preferred_channel]

        # Construcción de la cadena de responsabilidad
        chain_head = create_channel(ordered_channels[0])  # Crea el primer canal (preferido)
        current = chain_head
        for ch_type in ordered_channels[1:]:
            # Enlaza los canales en la cadena: cada canal conoce al siguiente
            current = current.set_next(create_channel(ch_type))

        # Intenta enviar la notificación, canal por canal, hasta que uno tenga éxito
        current_handler = chain_head
        success = False

        while current_handler:
            # Intenta enviar la notificación por el canal actual
            delivered = current_handler.handle(user.name, message)

            # Registra el intento de envío, con resultado
            self.logger.log(f"Attempted channel '{current_handler.channel_type}' for user '{user.name}': {'Success' if delivered else 'Failure'}")

            if delivered:
                success = True
                break  # Termina si el envío fue exitoso

            # Avanza al siguiente canal en la cadena (si existe)
            current_handler = current_handler.next_channel if hasattr(current_handler, "next_channel") else None

        return success  # Devuelve True si al menos un canal logró entregar el mensaje

    
