from flask import Flask
import logging
import yaml
from flasgger import Swagger
from app.routes.user_routes import user_bp
from app.routes.notification_routes import notification_bp

# Configurar logging (solo una vez)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Cargar swagger.yaml
with open("swagger.yaml", "r") as f:
    swagger_template = yaml.safe_load(f)

swagger = Swagger(app, template=swagger_template)

# Registrar rutas
app.register_blueprint(user_bp)
app.register_blueprint(notification_bp)

@app.route("/")
def home():
    return {"message": "API de notificaciones activa"}

if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)
