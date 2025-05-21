import os
from flask import Flask, render_template, jsonify, request
import requests

app = Flask(__name__)

# Set your OpenAI and Bing News API keys here
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "YOUR_OPENAI_API_KEY")
BING_API_KEY = os.getenv("BING_API_KEY", "YOUR_BING_API_KEY")

def fetch_news(query="latest"):
    url = f"https://api.bing.microsoft.com/v7.0/news/search?q={query}&count=10"
    headers = {"Ocp-Apim-Subscription-Key": BING_API_KEY}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json().get('value', [])
    else:
        return []

def summarize_text(text):
    # Call OpenAI API to summarize text
    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "gpt-4",
        "messages": [{"role": "user", "content": f"Summarize this news in 2 sentences: {text}"}],
        "max_tokens": 100,
    }
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        summary = response.json()["choices"][0]["message"]["content"]
        return summary
    else:
        return text

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/api/news")
def api_news():
    query = request.args.get("q", "latest")
    news_items = fetch_news(query)
    ai_news = []
    for item in news_items:
        summary = summarize_text(item.get("description", ""))
        ai_news.append({
            "title": item.get("name"),
            "url": item.get("url"),
            "image": item.get("image", {}).get("thumbnail", {}).get("contentUrl"),
            "summary": summary
        })
    return jsonify(ai_news)

if __name__ == "__main__":
    app.run(debug=True)
