# strategy.py

class BaseNotificationStrategy:
    def execute(self, channel_chain, message, logger):
        raise NotImplementedError("Debes implementar el método execute.")

class HighPriorityStrategy(BaseNotificationStrategy):
    def execute(self, channel_chain, message, logger):
        logger.log("Usando estrategia de alta prioridad.")
        # Agregar prefijo para alta prioridad
        prefixed_message = f"[ALTA PRIORIDAD] {message}"
        result = channel_chain.handle(prefixed_message, logger)
        if "fallaron" in result.lower():
            logger.log("Error crítico: No se pudo enviar la notificación de alta prioridad.")
        return result

class LowPriorityStrategy(BaseNotificationStrategy):
    def execute(self, channel_chain, message, logger):
        logger.log("Usando estrategia de baja prioridad.")
        # Agregar prefijo para baja prioridad
        prefixed_message = f"[BAJA PRIORIDAD] {message}"
        return channel_chain.handle(prefixed_message, logger)

class NotificationStrategy:
    @staticmethod
    def get_strategy(priority):
        if priority == "high":
            return HighPriorityStrategy()
        else:
            return LowPriorityStrategy()
