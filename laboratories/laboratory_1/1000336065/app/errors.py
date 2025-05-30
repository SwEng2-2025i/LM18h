from flask import jsonify

class UserNotFoundError(Exception):
    status_code = 404
    def __init__(self, message="User not found", status_code=None, payload=None):
        super().__init__(message)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv

class InvalidUsageError(Exception):
    status_code = 400
    def __init__(self, message, status_code=None, payload=None):
        super().__init__(message)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv

def register_error_handlers(app):
    @app.errorhandler(UserNotFoundError)
    def handle_user_not_found(error):
        response = jsonify(error.to_dict())
        response.status_code = error.status_code
        return response

    @app.errorhandler(InvalidUsageError)
    def handle_invalid_usage(error):
        response = jsonify(error.to_dict())
        response.status_code = error.status_code
        return response
    
    @app.errorhandler(ValueError) # Catch general ValueErrors from model validation
    def handle_value_error(error):
        response = jsonify({"message": str(error)})
        response.status_code = 400
        return response