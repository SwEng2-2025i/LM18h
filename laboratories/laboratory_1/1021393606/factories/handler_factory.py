# Factory Method - Crea los handlers concretos según el canal recibido.

from handlers.email_handler import EmailHandler
from handlers.sms_handler import SmsHandler
from handlers.console_handler import ConsoleHandler
from handlers.phone_call_handler import PhoneCallHandler
from handlers.whatsapp_handler import WhatsAppHandler

class HandlerFactory:
    @staticmethod
    def create_handler(channel, next_handler=None):
        """
        Recibe el nombre del canal y el siguiente handler de la cadena.
        Devuelve el handler correspondiente.
        Si el canal no existe, devuelve el next_handler directamente (ignora el canal inválido).
        """
        if channel == "email":
            return EmailHandler(next_handler)
        elif channel == "sms":
            return SmsHandler(next_handler)
        elif channel == "console":
            return ConsoleHandler(next_handler)
        elif channel == "phone":
            return PhoneCallHandler(next_handler)
        elif channel == "whatsapp":
            return WhatsAppHandler(next_handler)
        else:
            # Si el canal no es válido, se salta
            return next_handler
