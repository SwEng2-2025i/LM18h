from channels.channel_handler import NotificationChannel

class User:
    def __init__(self, name, preferred_channel, available_channels):
        self.name = name
        self.preferred_channel = preferred_channel
        self.available_channels = available_channels

    def build_channel_chain(self):
        channel_objects = [NotificationChannel(name) for name in self.available_channels]

        # Armar la cadena dinámicamente
        for i in range(len(channel_objects) - 1):
            channel_objects[i].set_next(channel_objects[i + 1])

        # Devolver el canal inicial
        return channel_objects[0] if channel_objects else None
