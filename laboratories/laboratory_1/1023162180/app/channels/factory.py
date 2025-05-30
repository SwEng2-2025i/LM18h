from app.channels.email import EmailChannel     
from app.channels.sms import SMSChannel         
from app.channels.console import ConsoleChannel 

# Diccionario que relaciona el nombre del canal con su clase correspondiente
_channel_map = {
    "email": EmailChannel,      # 'email' se asocia a EmailChannel
    "sms": SMSChannel,          # 'sms' se asocia a SMSChannel
    "console": ConsoleChannel,  # 'console' se asocia a ConsoleChannel
}

def create_channel(channel_type):
    # Obtiene la clase del canal según el tipo recibido
    channel_cls = _channel_map.get(channel_type)
    if not channel_cls:  # Si el tipo no existe en el diccionario, lanza un error
        raise ValueError(f"Unknown channel: {channel_type}")
    return channel_cls() # Devuelve una instancia de la clase del canal solicitado