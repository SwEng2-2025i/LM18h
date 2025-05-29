# Importamos la clase base que maneja la lógica de envío y el encadenamiento de canales
from app.core.handler import ChannelHandler

# Implementamos una clase tipo "Factory" para encapsular la creación de canales
class ChannelFactory:
    @staticmethod
    def create_channel(name):
        """
        Devuelve una instancia de ChannelHandler con el nombre del canal especificado.
        Este método permite crear canales dinámicamente sin usar if/else por canal.
        """
        return ChannelHandler(name)
