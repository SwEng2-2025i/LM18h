from app.models.channels import EmailChannel, SMSChannel, ConsoleChannel

# Construye una cadena de canales de notificación (Chain of Responsibility)
def build_chain(channels, preferred_channel=None):
    channel_map = {
        "email": EmailChannel,
        "sms": SMSChannel,
        "console": ConsoleChannel
    }
    
    # Coloca el canal preferido al inicio si está especificado y presente en la lista
    if preferred_channel and preferred_channel in channels:
        channels = [preferred_channel] + [ch for ch in channels if ch != preferred_channel]
    
    chain = None
    # Construye la cadena en orden inverso (el último canal apunta a None)
    for ch in reversed(channels):
        chain = channel_map[ch](successor=chain)
    return chain # Retorna el primer canal de la cadena