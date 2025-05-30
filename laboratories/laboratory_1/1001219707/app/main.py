from flask import Flask
from flasgger import Swagger

def create_app():
    """
    Crea la instancia principal de la aplicación Flask
    y registra los blueprints correspondientes.
    """
    app = Flask(__name__)
    Swagger(app)

    # Importar y registrar los módulos
    from .user import user_bp
    from .notification import notif_bp

    app.register_blueprint(user_bp)
    app.register_blueprint(notif_bp)

    return app

# Punto de entrada de la app
app = create_app()

if __name__ == '__main__':
    app.run(debug=True)