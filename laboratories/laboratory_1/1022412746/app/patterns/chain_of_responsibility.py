from app.utils import simulate_failure

class ChannelHandler:
    def __init__(self, name):
        self.name = name
        self.next = None

    def set_next(self, handler):
        self.next = handler
        return handler

    def handle(self, message, logger):
        logger.log(f"Intentando enviar por {self.name}...")
        if simulate_failure():
            logger.log(f"Envío por {self.name} exitoso.")
            return f"Notificación enviada por {self.name}"
        else:
            logger.log(f"Fallo al enviar por {self.name}.")
            if self.next:
                return self.next.handle(message, logger)
            else:
                return "Todos los canales fallaron."

def create_channel_chain(channels, preferred):
    ordered = sorted(channels, key=lambda ch: 0 if ch.name == preferred else 1)
    head = ordered[0]
    current = head
    for ch in ordered[1:]:
        current = current.set_next(ch)
    return head
