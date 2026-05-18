import json
import os
from output_formatter import OutputFormatter

# Correct dummy data structure for OutputFormatter
results = {
    "AAPL": {
        "stock_data": {
            "current_price": 150.00,
            "previous_close": 145.00,
            "change_percent": 3.45,
            "trend": "bullish",
            "volatility": "low",
            "data_source": "Yahoo Finance"
        },
        "summary": "Apple stocks are rising.",
        "sentiment": {
            "overall_sentiment": "Positive",
            "confidence": 0.85,
            "positive_articles": 10,
            "neutral_articles": 2,
            "negative_articles": 0
        },
        "insights": ["Bullish trend", "Strong market presence"]
    }
}

# Test HTML generation
try:
    print("Attempting to import OutputFormatter...")
    # Import is already done above
    print("Import successful.")
    
    formatter = OutputFormatter(results)
    html = formatter.generate_html_report()
    
    if html:
        print(f"HTML length: {len(html)}")
        print(f"First 100 chars: {html[:100]}")
    else:
        print("HTML is empty.")
except Exception as e:
    print(f"Error during execution: {e}")
