import random

class NotificationChannel:
    def __init__(self, successor=None):
        self.successor = successor

    def send(self, message, user):
        raise NotImplementedError("Método abstracto")

    def handle(self, message, user):
        success = self.send(message, user)
        if not success and self.successor:
            print(f"[{self.__class__.__name__}] Falló, probando siguiente canal...")
            self.successor.handle(message, user)
