"""
Step 2: Fetch Related Articles
Supports both real NewsAPI and mock data.
Set USE_REAL_APIS=true and NEWSAPI_KEY in .env to use real data.
"""

import random
from datetime import datetime, timedelta
import os
import time
import requests
from dotenv import load_dotenv

load_dotenv()

# Configuration
USE_REAL_APIS = os.getenv("USE_REAL_APIS", "false").lower() == "true"
NEWSAPI_KEY = os.getenv("NEWSAPI_KEY", "")
NEWSAPI_URL = "https://newsapi.org/v2/everything"


def _warn(message: str):
    """Print ASCII-only warnings so Windows presentation consoles do not crash."""
    print(f"[WARN] {message}")


def _demo_rng(ticker: str, count: int) -> random.Random:
    """Return a same-day deterministic RNG for stable presentation demos."""
    today = datetime.now().strftime("%Y-%m-%d")
    return random.Random(f"{ticker}:{count}:{today}:article-demo")

def get_real_articles(ticker: str, count: int = 3) -> list:
    """
    Fetch real news articles from NewsAPI.
    Requires: NEWSAPI_KEY in .env
    
    Free tier: 450 requests per day
    """
    if not NEWSAPI_KEY:
        _warn("NEWSAPI_KEY not set. Falling back to mock data.")
        return get_mock_articles(ticker, count)
    
    try:
        params = {
            "q": ticker,
            "sortBy": "publishedAt",
            "language": "en",
            "apiKey": NEWSAPI_KEY,
            "pageSize": count
        }
        
        response = requests.get(NEWSAPI_URL, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        if data.get("status") != "ok":
            _warn(f"NewsAPI Error: {data.get('message', 'Unknown error')}. Using mock data.")
            return get_mock_articles(ticker, count)
        
        articles = []
        for article in data.get("articles", [])[:count]:
            articles.append({
                "title": article.get("title", "N/A"),
                "description": article.get("description", ""),
                "published_at": article.get("publishedAt", ""),
                "source": article.get("source", {}).get("name", "Unknown"),
                "url": article.get("url", ""),
                "content": article.get("content", "")
            })
        
        # Respect rate limits
        time.sleep(0.1)
        
        return articles if articles else get_mock_articles(ticker, count)
    
    except requests.exceptions.RequestException as e:
        _warn(f"API request failed: {e}. Using mock data.")
        return get_mock_articles(ticker, count)
    except (ValueError, KeyError) as e:
        _warn(f"Could not parse API response: {e}. Using mock data.")
        return get_mock_articles(ticker, count)


def get_mock_articles(ticker: str, count: int = 3) -> list:
    """
    Simulates fetching news articles about a stock.
    
    Args:
        ticker: Stock symbol
        count: Number of articles to fetch
    
    Returns:
        List of article dictionaries
    """
    
    sample_headlines = [
        f"{ticker} Surges After Strong Earnings Report",
        f"Analysts Raise Price Target for {ticker}",
        f"{ticker} Faces Market Headwinds in Q4",
        f"Insider Trading Activity Detected in {ticker}",
        f"{ticker} Launches New Product Line",
        f"Market Rally Benefits {ticker} Stock",
        f"Regulatory Challenges Could Impact {ticker}",
        f"{ticker} Expands International Operations",
    ]
    
    sample_descriptions = [
        "Company announced record-breaking quarterly earnings with strong growth projections.",
        "Major investment firms increased their positions in the stock.",
        "Market volatility impacts valuations across the sector.",
        "Strategic partnerships could drive future revenue.",
        "Industry experts weigh in on recent developments.",
        "The stock shows resilience despite broader market concerns.",
        "New technology may disrupt the competitive landscape.",
    ]
    
    rng = _demo_rng(ticker, count)
    articles = []
    for i in range(count):
        pub_date = datetime.now() - timedelta(days=rng.randint(0, 7))
        articles.append({
            "title": rng.choice(sample_headlines),
            "description": rng.choice(sample_descriptions),
            "published_at": pub_date.strftime("%Y-%m-%d %H:%M:%S"),
            "source": rng.choice(["Bloomberg", "Reuters", "CNBC", "MarketWatch"]),
            "url": f"https://example-news.com/article-{i}"
        })
    
    return articles


def get_stock_articles(ticker: str, count: int = 3) -> list:
    """
    Get articles using real API or mock data.
    Automatically uses real API if configured, falls back to mock.
    """
    if USE_REAL_APIS:
        return get_real_articles(ticker, count)
    else:
        return get_mock_articles(ticker, count)


def format_articles_for_processing(articles: list) -> str:
    """
    Formats articles into a single string for LLM processing.
    
    Args:
        articles: List of article dictionaries
    
    Returns:
        Formatted string of articles
    """
    formatted = "ARTICLES:\n" + "=" * 50 + "\n\n"
    
    for i, article in enumerate(articles, 1):
        formatted += f"Article {i}:\n"
        formatted += f"Title: {article['title']}\n"
        formatted += f"Source: {article['source']}\n"
        formatted += f"Date: {article['published_at']}\n"
        formatted += f"Description: {article['description']}\n"
        formatted += "\n" + "-" * 50 + "\n\n"
    
    return formatted


if __name__ == "__main__":
    # Test the module
    articles = get_stock_articles("AAPL", count=3)
    print(f"Fetched {len(articles)} articles about AAPL:\n")
    print(format_articles_for_processing(articles))
