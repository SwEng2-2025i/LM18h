from flask import Flask, request, jsonify

def create_http_handler(use_case):
    app = Flask(__name__)

    @app.route("/tasks", methods=["POST"])
    def create_task():
        data = request.json
        task = use_case.create_task(data["title"])
        return jsonify({"id": task.id, "title": task.title, "done": task.done}), 201

    @app.route("/tasks", methods=["GET"])
    def list_tasks():
        tasks = use_case.get_all_tasks()
        return jsonify([{"id": t.id, "title": t.title, "done": t.done} for t in tasks])
    
    @app.route("/tasks/<id>/done", methods=["PUT"])
    def mark_done(id):
        use_case.update_task(id)
        return jsonify({}, 200)

    return app
