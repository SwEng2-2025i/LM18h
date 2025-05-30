from flask_restx import Namespace, Resource, fields
from app.routes.shared_data import users
from app.services.notifier import NotifierService

# Se crea un Namespace para agrupar las rutas relacionadas con notificaciones.
# Esto permite una mejor organización y separación en la documentación Swagger.
api = Namespace("Notifications", path="/notifications")

# Se instancia el servicio responsable de enviar notificaciones.
notifier = NotifierService()

# Se define el modelo de datos esperado en el cuerpo de la solicitud POST.
# Este modelo sirve tanto para validación como para la documentación automática.
notification_model = api.model("Notification", {
    "user_name": fields.String(required=True),
    "message": fields.String(required=True),
    "priority": fields.String(required=True)
})

# Se define la ruta "/notifications/send" que recibirá solicitudes POST.
@api.route("/send")
class NotificationSender(Resource):

    @api.expect(notification_model)  # Indica que se espera un cuerpo que siga el modelo definido
    @api.doc("Send a notification with fallback channels")  # Descripción visible en Swagger
    def post(self):
        # Se extraen los datos del cuerpo de la solicitud
        data = api.payload
        user_name = data["user_name"] 
        message = data["message"]
        priority = data["priority"]

        # Se busca el usuario en la lista compartida de usuarios
        user = next((u for u in users if u.name == user_name), None)
        if not user:
            return {"error": "User not found"}, 404

        # Se llama al servicio para enviar la notificación con fallback
        success = notifier.send_notification(user, message)

        # Se devuelve una respuesta según si el envío fue exitoso o no
        if success:
            return {"message": "Notification sent successfully"}, 200
        else:
            return {"message": "All channels failed to deliver notification"}, 500
