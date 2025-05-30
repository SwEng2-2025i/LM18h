from app import create_app
from flasgger import Swagger  # Agrega esta línea

app = create_app()
swagger = Swagger(app)  # Inicializa Swagger

if __name__ == "__main__":
    print("🌐 Rutas disponibles:")
    print(app.url_map)
    app.run(debug=True)