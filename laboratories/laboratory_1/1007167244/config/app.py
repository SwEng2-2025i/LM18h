from flask import Flask
from flask_restful import Api
from flasgger import Swagger

def create_app():
    app = Flask(__name__)
    api = Api(app)
    
    # Configuración de Swagger
    template = {
        "swagger": "2.0",
        "info": {
            "title": "API de Notificaciones",
            "description": "API para gestionar usuarios y notificaciones",
            "version": "1.0.0",
            "contact": {
                "email": "bgalindez@unal.edu.co"
            }
        },
        "basePath": "/",
        "schemes": [
            "http",
            "https"
        ],
    }
    
    swagger = Swagger(app, template=template)
    
    return app, api 