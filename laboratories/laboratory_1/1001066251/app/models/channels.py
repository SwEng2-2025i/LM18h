import random
from services.logger import LoggerSingleton

class Channel:
    def __init__(self, next_channel=None):
        # Define el siguiente canal en la cadena (si lo hay)
        self.next = next_channel

    def send(self, user, message):
        # Método abstracto que debe ser implementado por cada canal
        raise NotImplementedError

class EmailChannel(Channel):
    def send(self, user, message):
        # Intenta enviar por email
        LoggerSingleton().log(f"Trying email for {user.name}")
        if random.choice([True, False]):
            return f"Email sent to {user.name}"
        elif self.next:
            # Si falla, pasa al siguiente canal
            return self.next.send(user, message)
        else:
            return f"All channels failed for {user.name}"

class SMSChannel(Channel):
    def send(self, user, message):
        # Intenta enviar por SMS
        LoggerSingleton().log(f"Trying SMS for {user.name}")
        if random.choice([True, False]):
            return f"SMS sent to {user.name}"
        elif self.next:
            return self.next.send(user, message)
        else:
            return f"All channels failed for {user.name}"

class ConsoleChannel(Channel):
    def send(self, user, message):
        # Intenta enviar por consola
        LoggerSingleton().log(f"Trying console for {user.name}")
        if random.choice([True, False]):
            return f"Console output sent to {user.name}"
        elif self.next:
            return self.next.send(user, message)
        else:
            return f"All channels failed for {user.name}"
