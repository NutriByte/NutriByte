import os
from flask import Flask, render_template, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/team')
def team():
    return render_template('team_page.html')

@app.route('/meal')
def meal():
    # Example of a generated meal plan (you can replace with your logic)
    meal_plan = "Breakfast: Oatmeal, Lunch: Salad, Dinner: Grilled Chicken"
    return render_template('meal.html', meal_plan=meal_plan)

@app.route('/workout')
def workout():
    #Example of a generated workout
    workout_plan = "Full Body Strength: Squats - 3 sets of 12 reps, Push-Ups - 3 sets of 12 reps, Planks - 3 sets of 30 seconds "
    return render_template('workout.html', workout_plan=workout_plan)

@app.route('/api/message')
def get_message():
    return jsonify({"message": "Hello from Flask!"})


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    print(f"Running on http://127.0.0.1:{port}/")  
    app.run(host='0.0.0.0', port=port, debug=True)
