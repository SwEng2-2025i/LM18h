from flask_swagger_ui import get_swaggerui_blueprint

# Ruta donde se mostrará la documentación Swagger
SWAGGER_URL = '/docs'

# Ruta del archivo swagger.json que contiene la especificación de la API
API_URL = '/static/swagger.yaml'

# Crea el blueprint para la interfaz Swagger UI
swagger_ui = get_swaggerui_blueprint(
    SWAGGER_URL,  # URL base para la UI
    API_URL,      # URL del archivo Swagger
    config={ 'app_name': "Taller: Multichannel Notification System" }  # Nombre que se muestra en la UI
)
