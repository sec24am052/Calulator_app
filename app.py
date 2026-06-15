from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient
import os

app = Flask(__name__)

# MongoDB Connection
client = MongoClient(os.getenv("mongodb+srv://sec24am052:Fire557@calculator-cluster.lscegwp.mongodb.net/?appName=Calculator-Cluster"))

db = client["calculator_db"]

history_collection = db["history"]

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/calculate", methods=["POST"])
def calculate():

    data = request.json

    num1 = float(data["num1"])
    num2 = float(data["num2"])
    operation = data["operation"]

    result = 0

    if operation == "+":
        result = num1 + num2

    elif operation == "-":
        result = num1 - num2

    elif operation == "*":
        result = num1 * num2

    elif operation == "/":
        result = num1 / num2

    # Save to MongoDB
    history_collection.insert_one({
        "num1": num1,
        "num2": num2,
        "operation": operation,
        "result": result
    })

    return jsonify({"result": result})

@app.route("/history")
def history():

    data = list(history_collection.find({}, {"_id": 0}))

    return jsonify(data)

if __name__ == "__main__":
    app.run(debug=True)