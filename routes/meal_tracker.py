import random
from flask import Blueprint, render_template, request, jsonify, session
from extensions import meals_collection, users_collection

bp = Blueprint('meal_tracker', __name__)

@bp.route('/meal')
def meal():
    return render_template('mealTracker.html')

@bp.route('/api/meals', methods=['GET', 'POST', 'DELETE'])
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

@bp.route('/api/generate-meal-plan')
def generate_meal_plan():
    try:
        base_meals = {
            'breakfast': list(meals_collection.find({'type': 'breakfast'})),
            'lunch': list(meals_collection.find({'type': 'lunch'})),
            'dinner': list(meals_collection.find({'type': 'dinner'})),
            'snack': list(meals_collection.find({'type': 'snack'}))
        }

        # Include custom meals if user is logged in
        if 'user' in session:
            user = users_collection.find_one({'username': session['user']})
            custom_meals = user.get('custom_meals', [])
            for meal in custom_meals:
                base_meals[meal['type']].append(meal)

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

# NEW: API endpoint for food search using your existing food_search.py
@bp.route('/api/food_search', methods=['GET'])
def api_food_search():
    query = request.args.get('query', '')
    if not query:
        return jsonify({"products": []})
    from food_search import search_food  # Import your existing function
    products = search_food(query)
    return jsonify({"products": products})
