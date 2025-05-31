from application.services.user_services import UserServices
from application.factories.user_factory import UserFactory
from application.services.notification_services import NotificationServices
from application.factories.notification_factory import NotificationFactory
from adapters.user_storage import InMemoryUserStorage
from adapters.notification_sender import NotificationSender
from adapters.http_handler import create_http_handler
from application.factories.notification_factory import NotificationFactory

if __name__ == "__main__":
    user_storage = InMemoryUserStorage()
    notification_sender = NotificationSender()
    user_factory = UserFactory()
    notification_factory = NotificationFactory()
    
    notification_services = NotificationServices(user_storage, notification_sender, notification_factory)
    user_services = UserServices(user_storage, user_factory)
    
    app = create_http_handler(user_services, notification_services)
    app.run(debug=True)