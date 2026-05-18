"""
Configuration for the Stock Analysis Workflow
Customize stocks, APIs, and output formats here
"""

import os
from dotenv import load_dotenv

load_dotenv()

# ═══════════════════════════════════════════════════════════════
# STOCKS TO ANALYZE
# ═══════════════════════════════════════════════════════════════

STOCKS = {
    "AAPL": {"name": "Apple Inc.", "sector": "Technology"},
    "MSFT": {"name": "Microsoft Corp.", "sector": "Technology"},
    "GOOGL": {"name": "Alphabet Inc.", "sector": "Technology"},
    "TSLA": {"name": "Tesla Inc.", "sector": "Automotive"},
    "AMZN": {"name": "Amazon.com Inc.", "sector": "E-Commerce"},
    "NFLX": {"name": "Netflix Inc.", "sector": "Entertainment"},
}

# ═══════════════════════════════════════════════════════════════
# OUTPUT FORMATS
# ═══════════════════════════════════════════════════════════════

OUTPUT_FORMATS = {
    "text": True,      # report.txt
    "json": True,      # data.json + results.json
    "html": True,      # report.html (web view)
    "csv": True,       # stocks.csv (spreadsheet)
}

# ═══════════════════════════════════════════════════════════════
# API CONFIGURATION
# ═══════════════════════════════════════════════════════════════

# Use real APIs or mock data?
USE_REAL_APIS = os.getenv("USE_REAL_APIS", "false").lower() == "true"

# Stock Data API (Alpha Vantage)
ALPHAVANTAGE_API_KEY = os.getenv("ALPHAVANTAGE_API_KEY", "")
ALPHAVANTAGE_ENABLED = bool(ALPHAVANTAGE_API_KEY) and USE_REAL_APIS

# News API (NewsAPI.org)
NEWSAPI_KEY = os.getenv("NEWSAPI_KEY", "")
NEWSAPI_ENABLED = bool(NEWSAPI_KEY) and USE_REAL_APIS

# LLM API (OpenAI)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_ENABLED = bool(OPENAI_API_KEY) and USE_REAL_APIS

# ═══════════════════════════════════════════════════════════════
# API RATE LIMITS (to avoid hitting limits)
# ═══════════════════════════════════════════════════════════════

ALPHAVANTAGE_DELAY = 0.5  # seconds between requests (free tier = 5/min)
NEWSAPI_DELAY = 0.1       # NewsAPI allows 450/day
OPENAI_MAX_TOKENS = 500   # Keep responses reasonable

# ═══════════════════════════════════════════════════════════════
# REPORT CUSTOMIZATION
# ═══════════════════════════════════════════════════════════════

REPORT_TITLE = "Stock Analysis Report"
SHOW_CONFIDENCE_SCORES = True
INCLUDE_TECHNICAL_ANALYSIS = True
INCLUDE_PRICE_TARGETS = False  # Requires more advanced data

# ═══════════════════════════════════════════════════════════════
# HELPER FUNCTIONS
# ═══════════════════════════════════════════════════════════════

def get_selected_stocks(limit=None):
    """Get list of stocks to analyze."""
    stocks = list(STOCKS.keys())
    if limit:
        stocks = stocks[:limit]
    return stocks

def get_api_status():
    """Check which APIs are enabled."""
    status = {
        "use_real_apis": USE_REAL_APIS,
        "alphavantage": ALPHAVANTAGE_ENABLED,
        "newsapi": NEWSAPI_ENABLED,
        "openai": OPENAI_ENABLED,
    }
    return status

def print_config():
    """Print current configuration."""
    print("\n" + "=" * 60)
    print("WORKFLOW CONFIGURATION")
    print("=" * 60)
    print(f"\nStocks to analyze: {', '.join(get_selected_stocks())}")
    print(f"\nOutput formats:")
    for fmt, enabled in OUTPUT_FORMATS.items():
        status = "OK" if enabled else "DISABLED"
        print(f"  {fmt:8} {status}")
    
    print(f"\nAPI Status:")
    status = get_api_status()
    for api, enabled in status.items():
        if api != "use_real_apis":
            symbol = "[ON]" if enabled else "[OFF]"
            print(f"  {symbol} {api:15} {'Ready' if enabled else 'Not configured'}")
    
    print("\n" + "=" * 60 + "\n")

if __name__ == "__main__":
    print_config()
