# notification_handler.py
# Módulo encargado de construir la cadena de canales y enviar notificaciones a los usuarios.

from app.channels.email_channel import EmailChannel
from app.channels.sms_channel import SMSChannel
from app.channels.console_channel import ConsoleChannel

def build_channel_chain(preferred, available):
    """
    Construye la cadena de responsabilidad de canales de notificación.
    El canal preferido se coloca al inicio y los demás se agregan en orden.
    :param preferred: Canal preferido (str)
    :param available: Lista de canales disponibles (list)
    :return: Instancia del primer canal de la cadena
    """
    # Mapeo de string→clase
    mapping = {
        "email": EmailChannel,
        "sms": SMSChannel,
        "console": ConsoleChannel
    }
    # Primero el canal preferido
    head = mapping[preferred]()
    current = head
    # Luego los demás canales en orden, evitando duplicar el preferido
    for ch in available:
        if ch != preferred and ch in mapping:
            current = current.set_next(mapping[ch]())
    return head

def send_notification(user_name, message, user_cfg):
    """
    Envía una notificación a un usuario usando la cadena de canales.
    :param user_name: Nombre del usuario
    :param message: Mensaje a enviar
    :param user_cfg: Configuración del usuario (diccionario con 'preferred' y 'available')
    :return: True si se entregó, False si falló en todos los canales
    """
    chain = build_channel_chain(user_cfg["preferred"], user_cfg["available"])
    return chain.notify(user_name, message)
