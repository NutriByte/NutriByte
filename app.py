import os
from flask import Flask
from routes import home, auth, chatbot, meal_tracker
from extensions import initialize_database

app = Flask(__name__)
app.secret_key = os.urandom(24)  # Required for session management

# Initialize the database (sample meals, etc.)
initialize_database()

# Register Blueprints (each blueprint holds a section of the routes)
app.register_blueprint(home.bp)
app.register_blueprint(auth.bp)
app.register_blueprint(chatbot.bp)
app.register_blueprint(meal_tracker.bp)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5002))
    print(f"Running on http://127.0.0.1:{port}/")
    app.run(host='0.0.0.0', port=port, debug=True)
