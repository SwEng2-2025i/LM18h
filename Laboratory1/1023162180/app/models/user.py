class User:
    # Clase que representa un usuario con su nombre y preferencias de canales de comunicación
    def __init__(self, name, preferred_channel, available_channels):
        # Inicializa una instancia de User con:
        # - name: nombre único del usuario
        # - preferred_channel: canal de comunicación preferido para notificaciones
        # - available_channels: lista de canales de comunicación disponibles para ese usuario
        self.name = name
        self.preferred_channel = preferred_channel
        self.available_channels = available_channels