from functools import wraps
from flask import jsonify, request

# Decorador para requerir el encabezado Authorization en las peticiones
def require_authorization(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get("Authorization")

        # Retorna error si falta el encabezado Authorization
        if not auth_header:
            return jsonify({"error": "The Authorization header is missing"}), 401
        return f(*args, **kwargs)
    return decorated