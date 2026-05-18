"""
Step 1: Retrieve Stock Data
Supports both real Alpha Vantage API and mock data.
Set USE_REAL_APIS=true and ALPHAVANTAGE_API_KEY in .env to use real data.
"""

from datetime import datetime, timedelta
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

def get_real_stock_data(ticker: str) -> dict:
    """
    Fetch real stock data from Alpha Vantage API.
    Requires: ALPHAVANTAGE_API_KEY in .env
    
    Free tier: 5 requests per minute, 500 per day
    """
    if not ALPHAVANTAGE_API_KEY:
        print(f"⚠️  ALPHAVANTAGE_API_KEY not set. Falling back to mock data.")
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
            print(f"⚠️  API Error: {data['Error Message']}. Using mock data.")
            return get_mock_stock_data(ticker)
        
        if "Global Quote" not in data or not data["Global Quote"]:
            print(f"⚠️  No data for {ticker}. Using mock data.")
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
        print(f"⚠️  API request failed: {e}. Using mock data.")
        return get_mock_stock_data(ticker)
    except (ValueError, KeyError) as e:
        print(f"⚠️  Could not parse API response: {e}. Using mock data.")
        return get_mock_stock_data(ticker)


def get_mock_stock_data(ticker: str) -> dict:
    """
    Simulates stock data for testing without API keys.
    Generates realistic-looking but random data.
    """
    base_price = random.uniform(100, 500)
    prices = []
    dates = []
    
    for i in range(5):
        date = datetime.now() - timedelta(days=i)
        dates.append(date.strftime("%Y-%m-%d"))
        price = base_price + random.uniform(-5, 5)
        prices.append(round(price, 2))
    
    trend = "up" if prices[0] > prices[-1] else "down"
    change = round(((prices[0] - prices[-1]) / prices[-1]) * 100, 2)
    
    return {
        "ticker": ticker,
        "current_price": prices[0],
        "previous_close": prices[1],
        "change": round(prices[0] - prices[1], 2),
        "change_percent": change,
        "trend": trend,
        "volatility": "high" if abs(change) > 5 else "medium" if abs(change) > 2 else "low",
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
