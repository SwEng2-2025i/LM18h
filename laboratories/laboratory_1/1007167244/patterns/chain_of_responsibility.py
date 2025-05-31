from patterns.strategy import NotificationContext
import uuid

class MessageHandler:
    def __init__(self):
        self._next_handler = None

    def set_next(self, handler):
        self._next_handler = handler
        return handler

    def handle(self, message):
        if self._next_handler:
            return self._next_handler.handle(message)
        return message

class ContentValidator(MessageHandler):
    def handle(self, message):
        # Validar contenido inapropiado
        inappropriate_words = ["bad", "inappropriate", "spam"]
        if any(word in message.get('message', '').lower() for word in inappropriate_words):
            return {"error": "Message contains inappropriate content"}
        return super().handle(message)

class LengthValidator(MessageHandler):
    def handle(self, message):
        # Validar longitud del mensaje
        message_text = message.get('message', '')
        if len(message_text) > 500:
            return {"error": "Message is too long (max 500 characters)"}
        if len(message_text) < 1:
            return {"error": "Message cannot be empty"}
        return super().handle(message)

class PriorityHandler(MessageHandler):
    def handle(self, message):
        # Validar y procesar prioridad
        priority = message.get('priority', 'medium')
        if priority not in ['high', 'medium', 'low']:
            return {"error": "Invalid priority level"}
        return super().handle(message)

class DeliveryHandler(MessageHandler):
    def __init__(self, notification_context):
        super().__init__()
        self.notification_context = notification_context

    def handle(self, message):
        # Procesar la entrega del mensaje
        user = message.get('user')
        if not user:
            return {"error": "User not found"}
        
        notification_id = str(uuid.uuid4())
        result = self.notification_context.deliver_with_fallback(
            user,
            message.get('message', ''),
            notification_id,
            message.get('priority', 'medium')
        )
        return result 