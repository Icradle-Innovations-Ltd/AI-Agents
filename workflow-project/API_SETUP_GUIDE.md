# API Setup Guide

## Overview

This workflow can run with **mock data** (no API keys needed) or with **real APIs**. This guide walks you through both options.

---

## Option 1: Start with Mock Data (Recommended for Testing)

**Perfect for:** Learning, testing, development

### Setup (2 minutes)

1. **No setup needed!** The workflow uses mock data by default.

2. **Run the workflow:**
   ```bash
   python main_workflow.py
   ```

3. **View outputs:**
   - `output/report.txt` - Human-readable summary
   - `output/report.html` - Beautiful web view (open in browser)
   - `output/stocks.csv` - Spreadsheet format
   - `output/data.json` - Structured data

**Advantages:**
✓ No API keys needed
✓ Free to use
✓ Fast responses
✓ Great for testing

**Limitations:**
✗ Fake data (not real stock prices)
✗ Fake news articles
✗ Mock LLM responses

---

## Option 2: Use Real APIs (Production)

**Perfect for:** Real analysis, production use

### Step 1: Get API Keys

#### Stock Data - Alpha Vantage

1. Visit: https://www.alphavantage.co/
2. Click "GET FREE API KEY"
3. Fill in your email
4. Copy your API key

**Free Tier Details:**
- 5 requests per minute
- 500 requests per day
- Delay: 0.25 seconds between requests (built-in to workflow)

---

#### News Articles - NewsAPI

1. Visit: https://newsapi.org/
2. Click "Get API Key"
3. Sign up (free account)
4. Copy your API key

**Free Tier Details:**
- 450 requests per day
- Delay: 0.1 seconds between requests (built-in)

---

#### LLM - OpenAI (Optional)

1. Visit: https://platform.openai.com/api-keys
2. Sign up or log in
3. Create a new API key
4. Copy the key

**Note:** Real OpenAI calls cost money. Mock responses are free.

**Pricing:** ~$0.01 per 1000 tokens (small reports cost less than $0.001)

---

### Step 2: Configure the Workflow

1. **Copy the example environment file:**
   ```bash
   cp .env.example .env
   ```

2. **Edit `.env` and add your API keys:**
   ```env
   # Enable real APIs
   USE_REAL_APIS=true
   
   # Stock data
   ALPHAVANTAGE_API_KEY=your_key_here
   
   # News articles
   NEWSAPI_KEY=your_key_here
   
   # LLM (optional)
   OPENAI_API_KEY=your_key_here
   ```

3. **Save the file**

---

### Step 3: Run with Real APIs

```bash
python main_workflow.py
```

You should see:
```
✓ Stock data retrieved from Alpha Vantage
✓ Fetched 3 real articles about AAPL
✓ Real LLM summary generated
✓ Sentiment analysis completed
```

---

## Configuration Options

### Use Real APIs Selectively

You don't need all APIs! The workflow gracefully falls back to mock data if an API fails or is missing.

**Example: Use real stock data but mock news:**

```env
USE_REAL_APIS=true
ALPHAVANTAGE_API_KEY=your_key
# Leave NEWSAPI_KEY blank
# News will use mock data instead
```

---

### Add More Stocks to Analyze

Edit `config.py`:

```python
STOCKS = {
    "AAPL": {"name": "Apple Inc.", "sector": "Technology"},
    "MSFT": {"name": "Microsoft Corp.", "sector": "Technology"},
    "GOOGL": {"name": "Alphabet Inc.", "sector": "Technology"},
    "TSLA": {"name": "Tesla Inc.", "sector": "Automotive"},
    "AMZN": {"name": "Amazon.com Inc.", "sector": "E-Commerce"},
    "META": {"name": "Meta Platforms", "sector": "Technology"},
    "NVDA": {"name": "NVIDIA Corp.", "sector": "Technology"},
    # Add more...
}
```

Or customize in code:

```python
workflow = StockAnalysisWorkflow(stocks=["AAPL", "TSLA", "NVIDIA"])
```

---

### Customize Output Formats

Edit `config.py`:

```python
OUTPUT_FORMATS = {
    "text": True,      # report.txt
    "json": True,      # data.json
    "html": True,      # report.html (web view)
    "csv": True,       # stocks.csv (spreadsheet)
}
```

---

## Troubleshooting

### API Key Not Working?

1. **Check the .env file exists**
   ```bash
   ls -la .env
   ```

2. **Verify API key is correct**
   - Copy directly from the API provider website
   - No extra spaces or quotes

3. **Check rate limits**
   - Alpha Vantage: 5/min, 500/day
   - NewsAPI: 450/day
   - Wait 60 seconds if you hit limits

4. **Test the API directly**
   ```python
   import os
   from dotenv import load_dotenv
   load_dotenv()
   key = os.getenv("ALPHAVANTAGE_API_KEY")
   print(f"Key loaded: {key[:10]}...")  # Print first 10 chars
   ```

---

### "No module named 'requests'"?

Install it:
```bash
pip install -r requirements.txt
```

---

### API Returns "Invalid API key"?

1. Check `.env` has the correct key
2. Make sure you copied the full key (not partial)
3. Try a fresh key from the API provider
4. Wait a few minutes for the key to activate

---

### Workflow is Slow?

1. **Alpha Vantage rate limits** - Delay between requests is built-in (0.25s)
2. **NewsAPI daily limits** - You may have used your 450 daily requests
3. **OpenAI API calls** - First summarization may take 5-10 seconds

**Solution:** Try again tomorrow, or use mock data for faster testing.

---

## Cost Estimation

### Free Tier Costs

| Service | Free Limit | Cost Over Limit |
|---------|-----------|-----------------|
| Alpha Vantage | 5/min, 500/day | Free (just blocked) |
| NewsAPI | 450/day | Free (just blocked) |
| OpenAI | — | ~$0.001 per report |

**Running this workflow once/day = ~$0.03/month with OpenAI**

### Money-Saving Tips

1. **Use mock data for development** (free)
2. **Only enable OpenAI for final reports** (costs money)
3. **Cache results to avoid duplicate API calls**
4. **Use Alpha Vantage free tier** (500 req/day = fine for daily analysis)

---

## Advanced: Custom API Integrations

### Replace Alpha Vantage with IEX Cloud

1. Edit `stock_data.py`:
   ```python
   # Replace get_real_stock_data function with IEX Cloud API
   ```

2. Get API key: https://iexcloud.io/

### Add Email Notifications

1. Edit `output_formatter.py`:
   ```python
   # Add email sending after report generation
   ```

### Store Results in Database

1. Edit `main_workflow.py`:
   ```python
   # Add MongoDB/PostgreSQL storage after report generation
   ```

---

## Next Steps

1. **Test with mock data** → `python main_workflow.py`
2. **Get API keys** → Follow the steps above
3. **Configure .env** → Add your API keys
4. **Run with real data** → `python main_workflow.py`
5. **Customize** → Edit config.py for your needs
6. **Deploy** → Run on a schedule (cron, scheduler, cloud function)

---

## Questions?

Check the README.md for general workflow information.
