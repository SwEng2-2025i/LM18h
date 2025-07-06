from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

servicio_usuarios = Flask(__name__)
CORS(servicio_usuarios)

servicio_usuarios.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///usuarios.db'
servicio_usuarios.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(servicio_usuarios)

class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)

@servicio_usuarios.route('/usuarios', methods=['POST'])
def crear_usuario():
    datos = request.get_json()
    if not datos or 'nombre' not in datos or not datos['nombre'].strip():
        return jsonify({'error': 'El nombre es requerido'}), 400

    usuario = Usuario(nombre=datos['nombre'].strip())
    db.session.add(usuario)
    db.session.commit()
    print({'id': usuario.id, 'nombre': usuario.nombre})
    return jsonify({'id': usuario.id, 'nombre': usuario.nombre}), 201

@servicio_usuarios.route('/usuarios/<int:usuario_id>', methods=['GET'])
def obtener_usuario(usuario_id):
    usuario = Usuario.query.get(usuario_id)
    if usuario:
        return jsonify({'id': usuario.id, 'nombre': usuario.nombre})
    return jsonify({'error': 'Usuario no encontrado'}), 404

@servicio_usuarios.route('/usuarios', methods=['GET'])
def listar_usuarios():
    usuarios = Usuario.query.all()
    return jsonify([{'id': usuario.id, 'nombre': usuario.nombre} for usuario in usuarios])

@servicio_usuarios.route('/usuarios/<int:usuario_id>', methods=['DELETE'])
def eliminar_usuario(usuario_id):
    usuario = Usuario.query.get(usuario_id)
    if usuario is None:
        return jsonify({'error': 'Usuario no encontrado'}), 404
    
    db.session.delete(usuario)
    db.session.commit()
    return jsonify({'mensaje': f'Usuario {usuario_id} eliminado'}), 200

if __name__ == '__main__':
    with servicio_usuarios.app_context():
        db.create_all()
    servicio_usuarios.run(port=5001)
