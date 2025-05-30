from app.patterns.chain_of_responsibility import create_channel_chain, ChannelHandler
from app.patterns.factory import NotificationFactory
from app.patterns.singleton import LoggerSingleton
from app.patterns.strategy import NotificationStrategy
from app.services.user_service import UserService  # Importa el servicio de usuarios

class NotificationService:
    def __init__(self):
        self.logger = LoggerSingleton.get_instance()
        self.factory = NotificationFactory()
        self.user_service = UserService()  # Instancia el servicio de usuarios

    def send_notification(self, user_name, message, priority):
        user = self.user_service.get_user(user_name)
        if not user:
            return f"Usuario '{user_name}' no encontrado", 404

        channels = [ChannelHandler(name) for name in user["available_channels"]]
        chain = create_channel_chain(channels, user["preferred_channel"])

        self.logger.log(f"Enviando notificación con prioridad '{priority}' al usuario {user_name}")

        strategy = NotificationStrategy.get_strategy(priority)
        result = strategy.execute(chain, message, self.logger)

        self.logger.log(f"Resultado de la notificación: {result}")

        return result, 200
