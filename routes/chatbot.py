import openai
from flask import Blueprint, request, jsonify, render_template

bp = Blueprint('chatbot', __name__)

# OpenAI API Key (Replace with your actual API key)
OPENAI_API_KEY = "openai key here"
client = openai.OpenAI(api_key=OPENAI_API_KEY)

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

@bp.route('/chatbot')
def chatbot():
    return render_template('chatbot.html')

@bp.route("/api/chat", methods=["POST"])
def chat():
    try:
        data = request.json
        user_message = data.get("message", "").strip().lower()

        print(f"User message received: {user_message}")

        if not user_message:
            return jsonify({"reply": "Please type something to chat."})
        
        # Check for exercise video keywords
        for key in EXERCISE_VIDEOS:
            if key in user_message:
                video = EXERCISE_VIDEOS[key]
                return jsonify({
                    "reply": f"Here's a great {key} workout video for you:<br>"
                             f"<a href='{video['url']}' target='_blank'>"
                             f"<img src='{video['thumbnail']}' width='200'></a>"
                })
        
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

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            max_tokens=100
        )

        bot_reply = response.choices[0].message.content.strip()

        return jsonify({"reply": bot_reply})
    except openai.OpenAIError as e:
        print(f"OpenAI API Error: {e}")
        return jsonify({"reply": "I'm currently unavailable due to API limits. Try again later!"}), 500
    except Exception as e:
        print(f"Unexpected Error: {e}")
        return jsonify({"reply": "An unexpected error occurred. Please try again."}), 500
