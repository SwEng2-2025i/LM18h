class User:
    def __init__(self, name, preferred_channel, available_channels):
        # Inicializa el usuario con nombre, canal preferido y canales disponibles
        self.name = name
        self.preferred_channel = preferred_channel
        self.available_channels = available_channels

    def to_dict(self):
        # Devuelve una representación del usuario como diccionario
        return {
            'name': self.name,
            'preferred_channel': self.preferred_channel,
            'available_channels': self.available_channels
        }
