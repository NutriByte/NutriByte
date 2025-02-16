import os
from flask import Flask, render_template, jsonify

app = Flask(name)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/message')
def get_message():
    return jsonify({"message": "Hello from Flask!"})

if name == 'main':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)