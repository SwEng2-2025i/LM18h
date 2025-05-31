# swagger.py

def swagger_template():
    return {
        "swagger": "2.0",
        "info": {
            "title": "Multichannel Notification API",
            "description": "API para enviar notificaciones usando varios canales",
            "version": "1.0"
        },
        "basePath": "/",
        "schemes": ["http"],
    }

def swagger_config():
    return {
        "headers": [],
        "specs": [
            {
                "endpoint": 'apispec',
                "route": '/apispec.json',
                "rule_filter": lambda rule: True,
                "model_filter": lambda tag: True,
            }
        ],
        "static_url_path": "/flasgger_static",
        "swagger_ui": True,
        "specs_route": "/docs/"
    }
