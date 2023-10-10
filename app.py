import os
from flask import Flask, render_template, request
from datetime import datetime
import joblib
from newsapi import NewsApiClient
import mysql.connector

# Aiven config:
db_config = {
    "host": "mysql-pete-dbase-peterjmen-5ed9.aivencloud.com",
    "port": 25774,
    "user": "avnadmin",
    "password": "DB_PASSWORD", # Password in .ENV
    "database": "defaultdb",
    "ssl_ca": "/path/to/your/aiven_ca.pem",
}

app = Flask(__name__)
NEWS_API_KEY = "c90bf5366948496b842fa35d8776398c"
newsapi = NewsApiClient(api_key=NEWS_API_KEY)

# Load the trained model
base_directory = os.path.dirname(os.path.abspath(__file__))
model_filename = os.path.join(base_directory, "sentiment_model.pkl")
model = joblib.load(model_filename)
print(f"Trained model loaded from '{model_filename}'")

COUNTRY_MAP = {
    "USA": "us",
    "UK": "gb",
    "China": "cn",
    "New Zealand": "nz",
    "All Countries": None
}

def calculate_sentiment(title):
    probs = model.predict_proba([title])
    sentiment_value = 0 * probs[0][0] + 4 * probs[0][1]
    return sentiment_value

def sentiment_to_category(sentiment_value):
    if sentiment_value <= 0.5:
        return "Very Negative"
    elif sentiment_value <= 1.5:
        return "Negative"
    elif sentiment_value <= 2.5:
        return "Neutral"
    elif sentiment_value <= 3.5:
        return "Positive"
    else:
        return "Very Positive"

@app.route("/submit-rating", methods=["POST"])
def submit_rating():
    try:
        sentiment = request.form["sentiment"]
        article_title = request.form["article_title"]
        sentiment_map = {
            "Very Positive": 4,
            "Positive": 3,
            "Neutral": 2,
            "Negative": 1,
            "Very Negative": 0
        }
        insert_sentiment_to_db(sentiment, sentiment_map[sentiment], article_title)
        return "Rating submitted!", 200
    except Exception as e:
        print(f"Error encountered: {e}")
        return "An error occurred while processing your request.", 500

def insert_sentiment_to_db(sentiment, sentiment_value, article_title):
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        insert_query = """
        INSERT INTO sentifeed (sentiment, sentiment_value, article_headline)
        VALUES (%s, %s, %s)
        """
        cursor.execute(insert_query, (sentiment, sentiment_value, article_title))
        conn.commit()
    except Exception as e:
        print(f"Database insertion error: {e}")
        raise
    finally:
        cursor.close()
        conn.close()


@app.route("/", methods=["GET", "POST"])
def index():
    selected_country = request.form.get("country", "All Countries").strip()
    selected_category = request.form.get("category", "All News").strip()
    selected_sentiment = request.form.get("sentiment", "All Sentiment").strip()
    country_code = COUNTRY_MAP.get(selected_country)
    category_map = {
        "World": "general",
        "Finance": "business",
        "Sports": "sports",
        "Technology": "technology",
        "All News": None
    }
    category_code = category_map[selected_category]

    response = newsapi.get_top_headlines(
        country=country_code,
        category=category_code,
        language='en',
        page_size=100
    )
    articles = response.get("articles", [])

    for article in articles:
        article["headline"] = article["title"]
        article["date"] = datetime.strptime(article["publishedAt"], "%Y-%m-%dT%H:%M:%SZ").strftime("%b %d, %Y %H:%M:%S")
        sentiment_value = calculate_sentiment(article["title"])
        article["sentiment"] = sentiment_to_category(sentiment_value)

    if selected_sentiment != "All Sentiment":
        articles = [article for article in articles if article["sentiment"] == selected_sentiment]

    return render_template("index.html", news=articles)

if __name__ == "__main__":
    app.run(debug=True)
