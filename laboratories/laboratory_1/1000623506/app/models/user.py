class User:
    def __init__(self, name, preferred_channel, available_channels):
        # Inicialización de las propiedades del usuario:
        # - name: Nombre del usuario.
        # - preferred_channel: Canal preferido para recibir notificaciones
        # - available_channels: Lista de canales disponibles para el usuario.
        self.name = name
        self.preferred_channel = preferred_channel
        self.available_channels = available_channels