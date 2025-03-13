import os
import openai
from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from pymongo import MongoClient
import random
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = os.urandom(24)  # Required for session management

# OpenAI API Key (Replace with your actual API key)
OPENAI_API_KEY = "openai key here"
client = openai.OpenAI(api_key=OPENAI_API_KEY)

# Connect to MongoDB (Update these with your actual credentials)
MONGODB_USERNAME = "deeana"  # Your MongoDB Atlas username
MONGODB_PASSWORD = "cs4800"  # Your actual password
MONGODB_CLUSTER = "cluster0.ntbba.mongodb.net"
MONGODB_URI = f"mongodb+srv://{MONGODB_USERNAME}:{MONGODB_PASSWORD}@{MONGODB_CLUSTER}/?retryWrites=true&w=majority"

try:
    client = MongoClient(MONGODB_URI)
    # Test the connection
    client.admin.command('ping')
    print("Successfully connected to MongoDB!")
    db = client['meal_planner']
    meals_collection = db['meals']
    users_collection = db['users']
except Exception as e:
    print(f"Error connecting to MongoDB: {e}")

# Add this function to initialize the database with sample meals
def initialize_database():
    try:
        # Check if collection is empty
        if meals_collection.count_documents({}) == 0:
            sample_meals = [
                {'type': 'breakfast', 'name': 'Oatmeal with berries and almonds'},
                {'type': 'breakfast', 'name': 'Scrambled eggs with toast'},
                {'type': 'breakfast', 'name': 'Greek yogurt parfait'},
                {'type': 'lunch', 'name': 'Grilled chicken salad'},
                {'type': 'lunch', 'name': 'Quinoa bowl with vegetables'},
                {'type': 'lunch', 'name': 'Turkey and avocado sandwich'},
                {'type': 'dinner', 'name': 'Salmon with roasted vegetables'},
                {'type': 'dinner', 'name': 'Vegetarian stir-fry with tofu'},
                {'type': 'dinner', 'name': 'Lean beef with sweet potato'},
                {'type': 'snack', 'name': 'Greek yogurt with honey'},
                {'type': 'snack', 'name': 'Apple slices with almond butter'},
                {'type': 'snack', 'name': 'Mixed nuts and dried fruits'}
            ]
            meals_collection.insert_many(sample_meals)
            print("Sample meals added to database!")
    except Exception as e:
        print(f"Error initializing database: {e}")

# Call the initialization function when the app starts
initialize_database()

# Predefined workout videos
EXERCISE_VIDEOS = {
    "abs": {
        "title": "10-Minute Abs Workout",
        "url": "https://www.youtube.com/watch?v=1919eTCoESo",
        "thumbnail": "https://img.youtube.com/vi/1919eTCoESo/mqdefault.jpg"
    },
    "legs": {
        "title": "Leg Day Workout",
        "url": "https://www.youtube.com/watch?v=XleNPRD8pAo",
        "thumbnail": "https://img.youtube.com/vi/XleNPRD8pAo/mqdefault.jpg"
    },
    "full body": {
        "title": "Full Body Home Workout",
        "url": "https://www.youtube.com/watch?v=fNn3ZfN1lyo",
        "thumbnail": "https://img.youtube.com/vi/fNn3ZfN1lyo/mqdefault.jpg"
    }
}

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/team')
def team():
    return render_template('team_page.html')

@app.route('/chatbot')
def chatbot():
    return render_template('chatbot.html')

@app.route("/api/chat", methods=["POST"])
def chat():
    try:
        # Get user input
        data = request.json
        user_message = data.get("message", "").strip().lower()

        print(f"User message received: {user_message}")

        if not user_message:
            return jsonify({"reply": "Please type something to chat."})

        # Check if user asks for an exercise video
        for key in EXERCISE_VIDEOS:
            if key in user_message:
                video = EXERCISE_VIDEOS[key]
                return jsonify({
                    "reply": f"Here's a great {key} workout video for you:<br>"
                             f"<a href='{video['url']}' target='_blank'>"
                             f"<img src='{video['thumbnail']}' width='200'></a>"
                })

        # Define chatbot behavior
        messages = [
            {"role": "system", "content": (
                "You are a helpful health and fitness assistant providing advice on nutrition, recipes, and workouts. "
                "If a user asks for a recipe, provide one with ingredients and a simple preparation method. "
                "If they ask for workout tips, provide practical exercises they can do at home. "
                "Keep responses short (under 80 words)."
            )},
            {"role": "user", "content": user_message}
        ]

        print(f"Sending request to OpenAI: {messages}")

        # Call OpenAI API
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            max_tokens=100  # Keep responses concise
        )

        bot_reply = response.choices[0].message.content.strip()

        return jsonify({"reply": bot_reply})

    except openai.OpenAIError as e:
        print(f"OpenAI API Error: {e}")
        return jsonify({"reply": "I'm currently unavailable due to API limits. Try again later!"}), 500
    except Exception as e:
        print(f"Unexpected Error: {e}")
        return jsonify({"reply": "An unexpected error occurred. Please try again."}), 500

@app.route('/meal')
def meal():
    return render_template('meal.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = users_collection.find_one({'username': username})
        if user and check_password_hash(user['password'], password):
            session['user'] = username
            return redirect(url_for('meal'))
        return render_template('login.html', error='Invalid credentials')
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if users_collection.find_one({'username': username}):
            return render_template('register.html', error='Username already exists')
        
        hashed_password = generate_password_hash(password)
        users_collection.insert_one({
            'username': username,
            'password': hashed_password,
            'custom_meals': []
        })
        
        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('home'))

@app.route('/api/meals', methods=['GET', 'POST', 'DELETE'])
def manage_meals():
    if 'user' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    if request.method == 'GET':
        user_meals = users_collection.find_one({'username': session['user']})
        return jsonify({'meals': user_meals.get('custom_meals', [])})
    
    elif request.method == 'POST':
        new_meal = request.json
        users_collection.update_one(
            {'username': session['user']},
            {'$push': {'custom_meals': new_meal}}
        )
        return jsonify({'message': 'Meal added successfully'})
    
    elif request.method == 'DELETE':
        meal_name = request.json.get('name')
        users_collection.update_one(
            {'username': session['user']},
            {'$pull': {'custom_meals': {'name': meal_name}}}
        )
        return jsonify({'message': 'Meal deleted successfully'})

@app.route('/api/generate-meal-plan')
def generate_meal_plan():
    try:
        # Get base meals from MongoDB
        base_meals = {
            'breakfast': list(meals_collection.find({'type': 'breakfast'})),
            'lunch': list(meals_collection.find({'type': 'lunch'})),
            'dinner': list(meals_collection.find({'type': 'dinner'})),
            'snack': list(meals_collection.find({'type': 'snack'}))
        }

        # If user is logged in, include their custom meals
        if 'user' in session:
            user = users_collection.find_one({'username': session['user']})
            custom_meals = user.get('custom_meals', [])
            for meal in custom_meals:
                base_meals[meal['type']].append(meal)

        # Generate random meal plan
        meal_plan = {
            'meals': [
                f"Breakfast: {random.choice(base_meals['breakfast'])['name']}",
                f"Lunch: {random.choice(base_meals['lunch'])['name']}",
                f"Dinner: {random.choice(base_meals['dinner'])['name']}",
                f"Snack: {random.choice(base_meals['snack'])['name']}"
            ]
        }

        return jsonify(meal_plan)
    except Exception as e:
        print(f"Error generating meal plan: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5002))
    print(f"Running on http://127.0.0.1:{port}/")
    app.run(host='0.0.0.0', port=port, debug=True)