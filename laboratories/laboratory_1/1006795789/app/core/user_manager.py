# user_manager.py
# Módulo encargado de la gestión de usuarios en memoria.

class UserManager:
    """
    Clase que actúa como repositorio de usuarios.
    Permite agregar, obtener y listar usuarios.
    """
    _users = {}  # Diccionario para almacenar los usuarios registrados

    @classmethod
    def add_user(cls, name, preferred, available):
        """
        Agrega un usuario al repositorio.
        :param name: Nombre del usuario
        :param preferred: Canal preferido
        :param available: Lista de canales disponibles
        """
        cls._users[name] = {
            "preferred": preferred,
            "available": available
        }

    @classmethod
    def get_user(cls, name):
        """
        Obtiene la configuración de un usuario por su nombre.
        :param name: Nombre del usuario
        :return: Diccionario con la configuración del usuario o None si no existe
        """
        return cls._users.get(name)

    @classmethod
    def list_users(cls):
        """
        Devuelve el diccionario completo de usuarios registrados.
        :return: Diccionario de usuarios
        """
        return cls._users
