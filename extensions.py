import os
from pymongo import MongoClient

# Connect to MongoDB (Update these with your actual credentials)
MONGODB_USERNAME = "deeana"      # Your MongoDB Atlas username
MONGODB_PASSWORD = "cs4800"        # Your actual password
MONGODB_CLUSTER = "cluster0.ntbba.mongodb.net"
MONGODB_URI = f"mongodb+srv://{MONGODB_USERNAME}:{MONGODB_PASSWORD}@{MONGODB_CLUSTER}/?retryWrites=true&w=majority"

MONGODB_USERNAME2 = "EP10"      # Your MongoDB Atlas username
MONGODB_PASSWORD2 = "NBdat10base2"        # Your actual password
MONGODB_CLUSTER2 = "nutribyte-db2.twgt7.mongodb.net"
MONGODB_URI2 = f"mongodb+srv://{MONGODB_USERNAME2}:{MONGODB_PASSWORD2}@{MONGODB_CLUSTER2}/?retryWrites=true&w=majority"


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

try:
    client2 = MongoClient(MONGODB_URI2)
    # Test the connection
    client.admin.command('ping')
    print("Successfully connected to MongoDB2!")
    db2 = client['NutriByte-DB2']
    posts_collection = db2["posts"]
    friends_collection = db2["friends"]
    groups_collection = db2["groups"]
    messages_collection = db2["messages"]
except Exception as e:
    print(f"Error connecting to MongoDB2: {e}")

def initialize_database():
    try:
        # If meals collection is empty, add sample meals
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
