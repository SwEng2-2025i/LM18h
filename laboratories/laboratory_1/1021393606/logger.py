#Definición del NotificationLogger - Patrón Singleton
class NotificationLogger:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(NotificationLogger, cls).__new__(cls)
            cls._instance.logs = []
        return cls._instance

    #Registro de los intentos de cada notificación
    def log_attempt(self, user, channel, message, success):
        entry = {
            "user": user.get("name", "<unknown>"),
            "channel": channel,
            "message": message,
            "status": "SUCCESS" if success else "FAILURE"
        }
        print(f"[LOGGER] {entry}")
        self.logs.append(entry)

    def get_logs(self):
        return self.logs
