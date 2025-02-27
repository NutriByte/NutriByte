import os
import openai
from flask import Flask, render_template, request, jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

# OpenAI API Key (Replace with your actual API key)
OPENAI_API_KEY = "openai key here"
client = openai.OpenAI(api_key=OPENAI_API_KEY)

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

@app.route('/scrape-recipes', methods=['GET'])
def scrape_recipes():
    query = request.args.get('query', 'healthy recipes').strip().replace(' ', '+')
    url = f"https://www.allrecipes.com/search/results/?wt={query}&sort=re"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"Failed to retrieve the web page: {str(e)}"}), 500

    # Parse HTML using BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')
    recipe_links = []
    
    # Extract recipe titles and URLs
    for article in soup.find_all('article', class_='fixed-recipe-card'):
        title_tag = article.find('span', class_='fixed-recipe-card__title-link')
        link_tag = article.find('a', class_='fixed-recipe-card__title-link')
        
        if title_tag and link_tag:
            recipe_links.append({
                "title": title_tag.text,
                "url": link_tag['href']
            })
    
    return jsonify({"recipes": recipe_links})


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5002))
    print(f"Running on http://127.0.0.1:{port}/")
    app.run(host='0.0.0.0', port=port, debug=True)
