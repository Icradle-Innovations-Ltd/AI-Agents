"""
Step 1: Retrieve Stock Data
Supports both real Alpha Vantage API and mock data.
Set USE_REAL_APIS=true and ALPHAVANTAGE_API_KEY in .env to use real data.
"""

from datetime import datetime
import random
import os
import time
import requests
from dotenv import load_dotenv

load_dotenv()

# Configuration
USE_REAL_APIS = os.getenv("USE_REAL_APIS", "false").lower() == "true"
ALPHAVANTAGE_API_KEY = os.getenv("ALPHAVANTAGE_API_KEY", "")
ALPHAVANTAGE_URL = "https://www.alphavantage.co/query"

MOCK_CHANGE_PROFILES = {
    "AAPL": 1.66,
    "MSFT": 0.8,
    "GOOGL": -1.2,
    "TSLA": -6.4,
    "AMZN": 2.4,
    "NFLX": 5.8,
}


def _warn(message: str):
    """Print ASCII-only warnings so Windows presentation consoles do not crash."""
    print(f"[WARN] {message}")


def _demo_rng(ticker: str) -> random.Random:
    """Return a same-day deterministic RNG for stable presentation demos."""
    today = datetime.now().strftime("%Y-%m-%d")
    return random.Random(f"{ticker}:{today}:stock-demo")

def get_real_stock_data(ticker: str) -> dict:
    """
    Fetch real stock data from Alpha Vantage API.
    Requires: ALPHAVANTAGE_API_KEY in .env
    
    Free tier: 5 requests per minute, 500 per day
    """
    if not ALPHAVANTAGE_API_KEY:
        _warn("ALPHAVANTAGE_API_KEY not set. Falling back to mock data.")
        return get_mock_stock_data(ticker)
    
    try:
        # Get current quote
        params = {
            "function": "GLOBAL_QUOTE",
            "symbol": ticker,
            "apikey": ALPHAVANTAGE_API_KEY
        }
        
        response = requests.get(ALPHAVANTAGE_URL, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        if "Error Message" in data:
            _warn(f"API Error: {data['Error Message']}. Using mock data.")
            return get_mock_stock_data(ticker)
        
        if "Global Quote" not in data or not data["Global Quote"]:
            _warn(f"No data for {ticker}. Using mock data.")
            return get_mock_stock_data(ticker)
        
        quote = data["Global Quote"]
        
        # Respect rate limits
        time.sleep(0.25)
        
        # Parse the response
        price = float(quote.get("05. price", 0))
        change = float(quote.get("09. change", 0))
        
        if price == 0:
            return get_mock_stock_data(ticker)
        
        change_percent = (change / float(quote.get("08. previous close", price))) * 100 if price else 0
        
        return {
            "ticker": ticker,
            "current_price": round(price, 2),
            "previous_close": round(float(quote.get("08. previous close", price)), 2),
            "change": round(change, 2),
            "change_percent": round(change_percent, 2),
            "trend": "up" if change > 0 else "down",
            "volatility": "high" if abs(change_percent) > 5 else "medium" if abs(change_percent) > 2 else "low",
            "timestamp": quote.get("07. latest trading day", "N/A"),
            "data_source": "Alpha Vantage API"
        }
    
    except requests.exceptions.RequestException as e:
        _warn(f"API request failed: {e}. Using mock data.")
        return get_mock_stock_data(ticker)
    except (ValueError, KeyError) as e:
        _warn(f"Could not parse API response: {e}. Using mock data.")
        return get_mock_stock_data(ticker)


def get_mock_stock_data(ticker: str) -> dict:
    """
    Simulates stock data for testing without API keys.
    Generates realistic-looking deterministic data for stable demos.
    """
    rng = _demo_rng(ticker)
    previous_close = round(rng.uniform(100, 500), 2)
    change_percent = MOCK_CHANGE_PROFILES.get(ticker, round(rng.uniform(-4.0, 4.0), 2))
    current_price = round(previous_close * (1 + (change_percent / 100)), 2)
    price_change = round(current_price - previous_close, 2)
    trend = "up" if change_percent >= 0 else "down"
    
    return {
        "ticker": ticker,
        "current_price": current_price,
        "previous_close": previous_close,
        "change": price_change,
        "change_percent": change_percent,
        "trend": trend,
        "volatility": "high" if abs(change_percent) > 5 else "medium" if abs(change_percent) > 2 else "low",
        "timestamp": datetime.now().strftime("%Y-%m-%d"),
        "data_source": "Mock Data (for testing)"
    }


def get_stock_data(ticker: str) -> dict:
    """
    Get stock data using real API or mock data.
    Automatically uses real API if configured, falls back to mock.
    """
    if USE_REAL_APIS:
        return get_real_stock_data(ticker)
    else:
        return get_mock_stock_data(ticker)


def get_multiple_stocks(tickers: list) -> dict:
    """Get data for multiple stocks."""
    return {ticker: get_stock_data(ticker) for ticker in tickers}


if __name__ == "__main__":
    # Test the module
    stock_data = get_stock_data("AAPL")
    print("Stock Data for AAPL:")
    print(f"  Current Price: ${stock_data['current_price']}")
    print(f"  Trend: {stock_data['trend'].upper()}")
    print(f"  Change: {stock_data['change_percent']}%")
    print(f"  Volatility: {stock_data['volatility']}")
