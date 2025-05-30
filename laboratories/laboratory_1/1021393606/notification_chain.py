# Construcción de Chain of Responsibility seguún los canales disponibles del usuario - Se apoya en la HandlerFactory para crear los handlers específicos
from factories.handler_factory import HandlerFactory

def build_notification_chain(available_channels):
    chain = None

    # Se recorren los canales en orden inverso para construir la cadena de manera que el primer canal de la lista quede al principio de la cadena
    for channel in reversed(available_channels):
        chain = HandlerFactory.create_handler(channel, chain)
    return chain
