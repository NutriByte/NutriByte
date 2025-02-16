import os
from flask import Flask, render_template, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/team')
def team():
    return render_template('team_page.html')

@app.route('/api/message')
def get_message():
    return jsonify({"message": "Hello from Flask!"})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    print(f"Running on http://127.0.0.1:{port}/")  
    app.run(host='0.0.0.0', port=port, debug=True)
