from flask import Flask, request, jsonify # Import necessary Flask modules for web handling, request parsing, and JSON responses.

def create_http_handler(use_case):
    """
    Creates and configures a Flask application to handle HTTP requests for task management.

    Args:
        use_case: An object providing the business logic for task operations.
    
    Returns:
        A Flask application instance.
    """
    app = Flask(__name__) # Initialize a new Flask application.

    @app.route("/tasks", methods=["POST"])
    def create_task():
        """
        Handles POST requests to /tasks to create a new task.
        Expects a JSON payload with a "title" field.
        Returns the created task as JSON with a 201 status code.
        """
        data = request.json # Get JSON data from the request body.
        task = use_case.create_task(data["title"]) # Use the use_case to create a task.
        # Return the created task's details as a JSON response with HTTP status 201 (Created).
        return jsonify({"id": task.id, "title": task.title, "done": task.done}), 201

    @app.route("/tasks", methods=["GET"])
    def list_tasks():
        """
        Handles GET requests to /tasks to retrieve all tasks.
        Returns a list of tasks as JSON.
        """
        tasks = use_case.get_all_tasks() # Use the use_case to get all tasks.
        # Return a list of tasks, formatted as JSON.
        return jsonify([{"id": t.id, "title": t.title, "done": t.done} for t in tasks])
    
    @app.route("/tasks/<task_id>/done", methods=["PUT"])
    def set_task_done(task_id):
        """
        Handles PUT requests to /tasks/<task_id>/done to mark a specific task as done.
        Returns the updated task as JSON with a 204 status code on success.
        Returns a 404 error if the task is not found.
        """
        try:
            task = use_case.set_task_done(task_id) # Use the use_case to mark the task as done.
            # Return the updated task's details as a JSON response with HTTP status 204 (No Content).
            return jsonify({"id": task.id, "title": task.title, "done": task.done}), 204
        except ValueError as e:
            # If the task is not found (ValueError raised by use_case), return a 404 error.
            return jsonify({"error": str(e)}), 404

    return app # Return the configured Flask application instance.

