import random

class NotificationStrategy:
    def deliver(self, user, message, notification_id, priority, attempt_number):
        raise NotImplementedError

    def get_channel_name(self):
        raise NotImplementedError

class EmailStrategy(NotificationStrategy):
    def deliver(self, user, message, notification_id, priority, attempt_number):
        # Simulación de envío por email
        success = random.random() > 0.3  # 70% de probabilidad de éxito
        return {
            "success": success,
            "channel": "email",
            "message": f"Email enviado a {user['name']}: {message}"
        }

    def get_channel_name(self):
        return "email"

class SmsStrategy(NotificationStrategy):
    def deliver(self, user, message, notification_id, priority, attempt_number):
        # Simulación de envío por SMS
        success = random.random() > 0.2  # 80% de probabilidad de éxito
        return {
            "success": success,
            "channel": "sms",
            "message": f"SMS enviado a {user['name']}: {message}"
        }

    def get_channel_name(self):
        return "sms"

class WhatsAppStrategy(NotificationStrategy):
    def deliver(self, user, message, notification_id, priority, attempt_number):
        # Simulación de envío por WhatsApp
        success = random.random() > 0.1  # 90% de probabilidad de éxito
        return {
            "success": success,
            "channel": "whatsapp",
            "message": f"WhatsApp enviado a {user['name']}: {message}"
        }

    def get_channel_name(self):
        return "whatsapp"

class NotificationContext:
    def __init__(self):
        self.strategies = {
            'email': EmailStrategy(),
            'sms': SmsStrategy(),
            'whatsapp': WhatsAppStrategy()
        }
        self.current_strategy = None

    def set_strategy(self, channel):
        if channel in self.strategies:
            self.current_strategy = self.strategies[channel]
            return True
        return False

    def deliver_notification(self, user, message, notification_id, priority, attempt_number):
        if not self.current_strategy:
            return {"success": False, "message": "No strategy set"}
        return self.current_strategy.deliver(user, message, notification_id, priority, attempt_number)

    def deliver_with_fallback(self, user, message, notification_id, priority):
        available_channels = user.get('available_channels', [])
        preferred_channel = user.get('preferred_channel')
        
        # Ordenar canales: preferido primero, luego los demás
        channels = [preferred_channel] + [c for c in available_channels if c != preferred_channel]
        
        for attempt_number, channel in enumerate(channels, 1):
            if self.set_strategy(channel):
                result = self.deliver_notification(user, message, notification_id, priority, attempt_number)
                if result["success"]:
                    return result
        return {"success": False, "message": "All delivery attempts failed"} 