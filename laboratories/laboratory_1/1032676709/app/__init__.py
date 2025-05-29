from flask import Flask, redirect
from flasgger import Swagger

# Inicializa la aplicación Flask
app = Flask(__name__)

# Inicializa Swagger para documentar la API automáticamente
swagger = Swagger(app)

# Ruta raíz que redirige a la documentación Swagger
@app.route('/')
def home():
    return redirect('/apidocs')

# Importa las rutas de la API desde el módulo correspondiente
from app.routes import api