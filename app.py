from flask import Flask, render_template, request, redirect, jsonify, url_for
from pymongo import MongoClient
from bson import ObjectId
import datetime

app = Flask(__name__)

# MongoDB Setup
client = MongoClient("mongodb+srv://Bash-Anno1:1234567890@cluster-1.zcyy0.mongodb.net/?retryWrites=true&w=majority&appName=Cluster-1")
db = client["annotation_db"]
tasks_collection = db["img_annotations"]
annotations_collection = db["annotations"]

# Route: Home Page
@app.route("/")
def home():
    return redirect(url_for("get_task"))

# Route: Get Annotation Task
@app.route("/task")
def get_task():
    task = tasks_collection.find_one({"status": "pending"})
    if task:
        return render_template("annotation.html", image_url=task["image_url"], task_id=task["_id"])
    else:
        return render_template("completed.html", message="No tasks available!")

# Route: Save Annotations
@app.route("/save", methods=["POST"])
def save_annotation():
    task_id = request.form.get("task_id")
    annotations = request.form.get("annotations")  # JSON string from the frontend

    if not task_id or not annotations:
        return jsonify({"error": "Task ID and annotations are required."}), 400

    # Save annotations in the database
    annotations_collection.insert_one({
        "task_id": ObjectId(task_id),
        "annotations": annotations,
        "timestamp": datetime.datetime.now()
    })

    # Update task status
    tasks_collection.update_one(
        {"_id": ObjectId(task_id)},
        {"$set": {"status": "completed"}}
    )

    return redirect(url_for("get_task"))

if __name__ == "__main__":
    app.run(debug=True, port=7500)
