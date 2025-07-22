import os
import requests

def get_news(category: str = "general") -> str:
    """
    Fetches the latest news headlines for a given category using the GNews API.
    """
    api_key = os.getenv("GNEWS_API_KEY")  # Store your GNews API key in .env
    if not api_key:
        return "No API key found for GNews."

    # GNews categories: general, world, nation, business, technology, entertainment, sports, science, health
    url = (
        f"https://gnews.io/api/v4/top-headlines?"
        f"category={category.lower()}&lang=en&max=5&token={api_key}"
    )
    try:
        response = requests.get(url, timeout=10)
        if response.status_code != 200:
            return f"Unable to fetch news: {response.text}"
        data = response.json()
        articles = data.get("articles", [])
        if not articles:
            return "No news articles found for this category."
        result = "\n\n".join(
            f"{article['title']}\n{article['url']}" for article in articles
        )
        return result
    except Exception as e:
        return f"Error fetching news: {e}"