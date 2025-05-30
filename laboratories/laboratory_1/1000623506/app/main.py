from flask import Flask
from flask_restx import Api
from app.controllers.user_controller import api as user_ns
from app.controllers.notification_controller import api as notification_ns
from app.controllers.logs_controller import api as logs_ns

# Creación de la instancia principal de Flask
app = Flask(__name__)
api = Api(app, version='1.0', title='Notification API', description='A multichannel notification system', doc='/')

# Registro de rutas
api.add_namespace(user_ns, path='/users')
api.add_namespace(notification_ns, path='/notifications')
api.add_namespace(logs_ns, path='/logs')


if __name__ == '__main__':
    app.run(debug=True)