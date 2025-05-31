# app/services/notification_service.py

from app.services.user_service import users
from app.patterns.channel_handlers import ChannelHandler

def send_notification(user_name, message):
    user = next((u for u in users if u.name == user_name), None)
    if not user:
        return {"error": "User not found"}, 404

    channels = user.available_channels
    preferred = user.preferred_channel

    # Creamos la cadena
    handlers = {}
    first_handler = None
    last_handler = None

    for ch in channels:
        handler = ChannelHandler(ch)
        handlers[ch] = handler
        if not first_handler:
            first_handler = handler
        if last_handler:
            last_handler.set_next(handler)
        last_handler = handler

    # Si el canal preferido no es el primero, lo movemos al frente
    if preferred in handlers and preferred != channels[0]:
        preferred_handler = handlers[preferred]
        # Reconstruimos la cadena empezando por el preferido
        remaining = [ch for ch in channels if ch != preferred]
        first_handler = preferred_handler
        current = preferred_handler
        for ch in remaining:
            current = current.set_next(handlers[ch])

    # Ejecutamos la cadena
    return first_handler.handle(user, message), 200
