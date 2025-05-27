from flask import Flask, request, jsonify

def create_http_handler(use_case):
    app = Flask(__name__)

    @app.route("/tasks", methods=["POST"])
    def create_task():
        data = request.json
        if not data or "title" not in data:
            return jsonify({"error": "Title is required"}), 400
        task = use_case.create_task(data["title"])
        return jsonify({"id": task.id, "title": task.title, "done": task.done}), 201

    @app.route("/tasks", methods=["GET"])
    def list_tasks():
        tasks = use_case.get_all_tasks()
        return jsonify([{"id": t.id, "title": t.title, "done": t.done} for t in tasks])

    @app.route("/tasks/<task_id>", methods=["GET"])
    def get_task(task_id):
        task = use_case.get_task_by_id(task_id)
        if task is None:
            return jsonify({"error": "Task not found"}), 404
        return jsonify({"id": task.id, "title": task.title, "done": task.done}), 200

    @app.route("/tasks/mark_done/<task_id>", methods=["POST"])
    def mark_task_done(task_id):
        use_case.mark_task_done(task_id)
        return jsonify({"message": "Task marked as done"}), 200
    return app
