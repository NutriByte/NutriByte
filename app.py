import os
from flask import Flask, request, jsonify, render_template
#from db import posts, users
from routes import home, auth, chatbot, meal_tracker
from extensions import initialize_database, posts_collection, friends_collection, groups_collection, messages_collection

app = Flask(__name__, static_folder='static', template_folder='templates')
app.secret_key = os.urandom(24)  # Required for session management
# Initialize the database (sample meals, etc.)
initialize_database()

# Register Blueprints (each blueprint holds a section of the routes)
app.register_blueprint(home.bp)
app.register_blueprint(auth.bp)
app.register_blueprint(chatbot.bp)
app.register_blueprint(meal_tracker.bp)

@app.route('/social/posts', methods=['GET'])
def get_posts():
    posts = list(posts_collection.find({}, {'_id': 0}))
    return jsonify(posts)

@app.route('/social/posts', methods=['POST'])
def create_post():
    data = request.json
    new_post = {
        "author": data.get("username"),
        "content": data.get("content"),
        "likes": [],
        "comments": []
    }
    posts_collection.insert_one(new_post)
    return jsonify({"message": "Post created"}), 201

@app.route('/social/like', methods=['POST'])
def like_post():
    data = request.json
    username = data.get("username")
    content = data.get("content")

    result = posts_collection.update_one(
        {"content": content},
        {"$addToSet": {"likes": username}}
    )
    return jsonify({"mmessage": "Likeed post"} if result.modified_count else {"message": "Already liked or not found"})

@app.route('/social/comment', methods=['POST'])
def comment_post():
    data = request.json
    comment = {
        "author": data.get("username"),
        "text": data.get("comment")
    }
    result = posts_collection.update_one(
        {"content": data.get("content")},
        {"$push": {"comments": comment}},
        
    )
    return jsonify({"message": "Comment added"} if result.modified_count else {"message": "Post not found"})

@app.route('/social/friends', methods=['POST'])
def add_friend():
    data = request.json
    username = data.get("username")
    friend = data.get("friend")

    friends_collection.update_one(
        {"username": username},
        {"$addToSet": {"friends": friend}},
        upsert=True
    )
    return jsonify({"message": f"{friend} added as friend"})

@app.route('/social/friends/<username>', methods=['GET'])
def get_friends(username):
    doc = friends_collection.find_one({"username": username}, {'_id': 0})
    return jsonify(doc or {"friends": []})

@app.route('/social/groups', methods=['POST'])
def join_group():
    data = request.json
    group = data.get("group")
    user = data.get("username")

    groups_collection.update_one(
        {"name": group},
        {"$addToSet": {"members": user}},
        upsert=True
    )

    return jsonify({"message": f"Joined/created group {group}"})

@app.route('/social/groups/<group>', methods=['GET'])
def get_group_members(group):
    doc = groups_collection.find_one({"name": group}, {'_id': 0})
    return jsonify(doc or {"members": []})

@app.route('/social/messages/send', methods=['POST'])
def send_message():
    data = request.json
    message = {
        "from": data.get("from"),
        "to": data.get("to"),
        "message": data.get("message"),
        "timestamp": data.get("timestamp") #optional
    }
    messages_collection.insert_one(message)
    return jsonify({"message": "Message sent"})

@app.route('/social/messages/<username>', methods=['GET'])
def get_messages(username):
    messages = list(messages_collection.find(
        {"$or": [{"from": username}, {"to": username}]},
        {'_id':0}
    ))
    return jsonify(messages)

@app.route('/')
def homepage():
    return render_template('index.html')

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    print(f"Running on http://127.0.0.1:{port}/")
    app.run(host='0.0.0.0', port=port, debug=True)
