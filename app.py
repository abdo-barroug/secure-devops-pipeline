import os

from flask import Flask, jsonify, request

app = Flask(__name__)

# Stockage simple en mémoire pour ce projet de démonstration.
tasks = []
next_task_id = 1


@app.get("/")
def home():
    return jsonify({
        "name": "Secure DevOps Pipeline API",
        "status": "running",
        "endpoints": ["/health", "/tasks"]
    })


@app.get("/health")
def health():
    return jsonify({"status": "healthy"}), 200


@app.get("/tasks")
def get_tasks():
    return jsonify(tasks), 200


@app.post("/tasks")
def create_task():
    global next_task_id

    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({"error": "A JSON object is required"}), 400

    title = data.get("title")

    if not isinstance(title, str) or not title.strip():
        return jsonify({"error": "A non-empty title is required"}), 400

    task = {
        "id": next_task_id,
        "title": title.strip(),
        "completed": False
    }

    tasks.append(task)
    next_task_id += 1

    return jsonify(task), 201


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    app.run(host="0.0.0.0", port=port)
