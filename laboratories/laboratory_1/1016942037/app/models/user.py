# Modelo de datos para representar un usuario del sistema

class User:
    def __init__(self, name, preferred_channel, available_channels):
        """
        Inicializa un nuevo usuario con su nombre, canal preferido y canales disponibles.

        :param name: Nombre del usuario (string)
        :param preferred_channel: Canal de comunicación preferido (string)
        :param available_channels: Lista de canales disponibles (lista de strings)
        """
        self.name = name  # Nombre del usuario
        self.preferred_channel = preferred_channel  # Canal principal que se intentará primero
        self.available_channels = available_channels  # Canales alternativos en orden de prioridad
