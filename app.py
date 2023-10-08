import os
from flask import Flask, render_template, request
from datetime import datetime
import joblib
from newsapi import NewsApiClient

app = Flask(__name__)
NEWS_API_KEY = "c90bf5366948496b842fa35d8776398c"
newsapi = NewsApiClient(api_key=NEWS_API_KEY)

# Update the path for the trained model
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


def calculate_sentiment(text):
    probs = model.predict_proba([text])
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


def fetch_articles(country=None, category=None, sentiment=None):
    print(f"Fetching articles for country: {country} and category: {category}")  # Debug print

    response = newsapi.get_top_headlines(
        country=country if country and country != "" else None,
        category=category,
        language='en',
        page_size=100
    )

    articles = response.get("articles", [])

    # Format the published date and analyze sentiment
    for article in articles:
        article["content"] = article["content"] or "No content available"
        article["publishedAt"] = datetime.strptime(
            article["publishedAt"], "%Y-%m-%dT%H:%M:%SZ"
        ).strftime("%b %d, %Y %H:%M:%S")

        sentiment_weighting = calculate_sentiment(article["content"])
        sentiment_category = sentiment_to_category(sentiment_weighting)

        article["sentiment_weighting"] = sentiment_weighting
        article["sentiment_category"] = sentiment_category

    # Sort articles by publishedAt in descending order
    sorted_articles = sorted(
        articles,
        key=lambda x: datetime.strptime(x["publishedAt"], "%b %d, %Y %H:%M:%S"),
        reverse=True,
    )

    # Filter articles based on the selected sentiment
    if sentiment and sentiment != "All":
        filtered_articles = [
            article
            for article in sorted_articles
            if article["sentiment_category"] == sentiment
        ]
    else:
        filtered_articles = sorted_articles

    return filtered_articles


@app.route("/", methods=["GET", "POST"])
def index():
    selected_country = request.form.get("country", "All Countries").strip()
    selected_category = request.form.get("category", "All News").strip()
    selected_sentiment = request.form.get("sentiment", "All Sentiment").strip()
    
    country_code = COUNTRY_MAP[selected_country]
    
    # Map category
    category_map = {
        "World": "general",
        "Finance": "business",
        "Sports": "sports",
        "Technology": "technology",
        "All News": None
    }
    category_code = category_map[selected_category]

    # Fetch the articles
    response = newsapi.get_top_headlines(
        country=country_code,
        category=category_code,
        language='en',
        page_size=100
    )
    
    articles = response.get("articles", [])

    # Format the published date and analyze sentiment for each article
    for article in articles:
        article["headline"] = article["title"]
        article["date"] = datetime.strptime(
            article["publishedAt"], "%Y-%m-%dT%H:%M:%SZ"
        ).strftime("%b %d, %Y %H:%M:%S")
        sentiment_value = calculate_sentiment(article["description"] or article["title"])
        article["sentiment"] = sentiment_to_category(sentiment_value)

    # If sentiment is selected, filter articles
    if selected_sentiment != "All Sentiment":
        articles = [article for article in articles if article["sentiment"] == selected_sentiment]

    return render_template(
        "index.html",
        news=articles
    )


if __name__ == "__main__":
    app.run(debug=True)
