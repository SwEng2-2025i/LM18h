# Clase base para todos los handlers de notificaciones - Patrón Chain of Responsibility
class BaseHandler: 
    #Constructor que recibe el siguiente handler en la cadena
    def __init__(self, next_handler=None):
        self.next_handler = next_handler

    def handle(self, user, message):
        raise NotImplementedError("Subclasses must implement handle()")
