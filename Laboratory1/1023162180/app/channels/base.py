import random  # Importa random (aunque no se usa aquí, puede ser útil en subclases)

class NotificationChannel:
    """
    Clase base abstracta que representa un canal de notificación en una cadena de responsabilidad.
    Cada canal puede manejar una notificación o pasarla al siguiente canal en la cadena.
    """

    def __init__(self):
        self.next_channel = None  # Inicializa el siguiente canal como None

    def set_next(self, channel):
        """
        Define el siguiente canal de notificación.
        Permite encadenar varios canales fácilmente.
        """
        self.next_channel = channel  # Asigna el siguiente canal
        return channel  # Permite encadenar: obj1.set_next(obj2).set_next(obj3)

    def handle(self, user_name, message):
        """
        Método abstracto que deben implementar las subclases.
        Si el canal no puede manejar la notificación, puede delegar al siguiente canal.
        """
        raise NotImplementedError("Must override handle() method")  # Obliga a implementar en subclases