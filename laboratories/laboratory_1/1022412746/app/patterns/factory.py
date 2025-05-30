# factory.py
class NotificationFactory:
    """
    Factory simple para crear objetos de notificación.
    En este ejemplo, solo devuelve un string o un objeto dummy,
    pero puedes extenderlo para crear diferentes tipos de notificaciones.
    """

    def create_notification(self, message, priority):
        # Aquí puedes crear diferentes clases de notificación según la prioridad o tipo.
        return {
            "message": message,
            "priority": priority
        }
