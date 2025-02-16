from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/")
def home():
    return "Hello, World!"

@app.route("/api/message")
def message():
    return jsonify({"message": "This is my first API response!"})

if __name__ == "__main__":
    app.run(debug=True)

