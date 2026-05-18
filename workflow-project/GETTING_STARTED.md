# Stock Analysis Workflow - Enhanced Edition

## What You Now Have

A **production-ready, customizable stock analysis workflow** that:

✓ Analyzes **multiple stocks** (6 by default: AAPL, MSFT, GOOGL, TSLA, AMZN, NFLX)
✓ Generates **4 output formats**:
  - Text reports (readable summaries)
  - HTML reports (beautiful web views)
  - CSV exports (spreadsheet-ready)
  - JSON data (programmatic access)

✓ Supports **real & mock APIs**:
  - Real stock data (Alpha Vantage)
  - Real news articles (NewsAPI)
  - Real LLM summaries (OpenAI)
  - Or mock data for testing (no API keys needed)

✓ **Fully customizable** via config files

---

## Quick Start (2 minutes)

### 1. Run with Mock Data (No API Keys)

```bash
cd workflow-project
python main_workflow.py
```

### 1b. Run the Agent Version

```bash
python main_workflow.py --agent
```

Optional: analyze specific tickers with the agent.

```bash
python main_workflow.py --agent --stocks AAPL MSFT
```

The agent also persists cross-run memory in `output/agent_memory.json`, so later runs can reuse prior lessons and planning history.

### 1c. Launch the UI Dashboard

```bash
streamlit run app.py
```

Use the dashboard to switch between workflow and agent mode, choose stocks, and inspect the latest outputs and persistent memory.

### 2. View the Results

```bash
# Text report (command line)
cat output/report.txt

# CSV (open in Excel)
open output/stocks.csv

# HTML (open in browser)
open output/report.html

# JSON (for programmatic use)
cat output/data.json
```

---

## File Structure

```
workflow-project/
├── config.py                  # Customize stocks & settings
├── main_workflow.py           # Run the workflow
├── stock_data.py              # Real/mock stock data
├── article_fetcher.py         # Real/mock articles
├── llm_processor.py           # Real/mock LLM
├── output_formatter.py        # Format outputs
├── API_SETUP_GUIDE.md         # How to get API keys
├── .env.example               # Environment template
├── requirements.txt           # Python dependencies
└── output/                    # Generated reports
    ├── report.txt
    ├── report.html
    ├── stocks.csv
    ├── data.json
    └── results.json
```

---

## Customization Guide

### 1. Add More Stocks

Edit `config.py`:

```python
STOCKS = {
    "AAPL": {"name": "Apple Inc.", "sector": "Technology"},
    "MSFT": {"name": "Microsoft Corp.", "sector": "Technology"},
    "GOOGL": {"name": "Alphabet Inc.", "sector": "Technology"},
    "TSLA": {"name": "Tesla Inc.", "sector": "Automotive"},
    "NVDA": {"name": "NVIDIA Corp.", "sector": "Technology"},  # Add more
    "COIN": {"name": "Coinbase Global", "sector": "Crypto"},    # Add more
}
```

### 2. Use Real APIs

See `API_SETUP_GUIDE.md` for detailed instructions:

1. Get API keys (free tiers available)
2. Copy `.env.example` to `.env`
3. Add your API keys to `.env`
4. Set `USE_REAL_APIS=true`

Example `.env`:

```
USE_REAL_APIS=true
ALPHAVANTAGE_API_KEY=demo  # Replace with your key
NEWSAPI_KEY=your_key_here
OPENAI_API_KEY=sk-...
```

### 3. Customize Output Formats

Edit `config.py`:

```python
OUTPUT_FORMATS = {
    "text": True,      # Enable/disable
    "json": True,
    "html": True,
    "csv": True,
}
```

### 4. Run Different Stocks Programmatically

```python
from main_workflow import StockAnalysisWorkflow

# Run specific stocks
workflow = StockAnalysisWorkflow(stocks=["TSLA", "META", "NFLX"])
workflow.run()
workflow.save_outputs("./output")
```

---

## Output Formats Explained

### Text Report (`report.txt`)

Human-readable summaries:

```
STOCK ANALYSIS REPORT
Generated: 2026-05-18 16:30:00
======================================================================

TICKER: AAPL
------
Current Price: $196.97
Change: 1.96%
Trend: UP
Volatility: low
Data Source: Mock Data

SUMMARY:
The articles discuss recent developments in the tech sector...

SENTIMENT ANALYSIS:
Overall: POSITIVE (Confidence: 0.85)
Positive Articles: 2
...

KEY INSIGHTS:
1. The stock is in an up trend...
2. Recent articles show positive sentiment...
```

### CSV Report (`stocks.csv`)

Spreadsheet-ready format:

```
Ticker,Price,Change %,Trend,Sentiment
AAPL,$196.97,1.96%,UP,positive
MSFT,$230.13,-2.81%,DOWN,positive
GOOGL,$...
```

Open in Excel/Google Sheets!

### HTML Report (`report.html`)

Beautiful web view with styling and metrics. Open in any browser.

### JSON Data (`data.json`)

Structured data for programs:

```json
{
  "generated": "2026-05-18T16:30:00",
  "stocks": {
    "AAPL": {
      "price": 196.97,
      "trend": "up",
      "insights": [...]
    }
  }
}
```

---

## Real API Integration

### Stock Data (Alpha Vantage)

Provides real-time stock prices, changes, and trends.

**Setup:**
1. Visit https://www.alphavantage.co/
2. Get free API key
3. Add to `.env`: `ALPHAVANTAGE_API_KEY=your_key`

**Free Tier:** 5 requests/min, 500/day

### News Articles (NewsAPI)

Fetches real articles about companies.

**Setup:**
1. Visit https://newsapi.org/
2. Get free API key
3. Add to `.env`: `NEWSAPI_KEY=your_key`

**Free Tier:** 450 requests/day

### LLM Summaries (OpenAI)

Generates intelligent summaries and analysis.

**Setup:**
1. Visit https://platform.openai.com/api-keys
2. Create API key (requires credit card)
3. Add to `.env`: `OPENAI_API_KEY=sk-...`

**Pricing:** ~$0.001 per report

---

## Advanced Usage

### Schedule Daily Runs

**Windows (Task Scheduler):**

```
Program: C:\Python\python.exe
Arguments: C:\path\to\workflow-project\main_workflow.py
```

**Linux/Mac (Cron):**

```bash
0 9 * * * cd /path/to/workflow-project && python main_workflow.py
```

### Send Email Reports

Add to `main_workflow.py`:

```python
import smtplib
from email.mime.text import MIMEText

# After workflow completes
report = workflow.generate_report()
msg = MIMEText(report)
msg['Subject'] = 'Daily Stock Analysis'
msg['From'] = 'your@email.com'
msg['To'] = 'recipient@email.com'

server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
server.login('your@email.com', 'app_password')
server.send_message(msg)
server.quit()
```

### Save to Database

Add to `main_workflow.py`:

```python
import json
from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017/')
db = client['stocks']
collection = db['analysis']

# Save results
data = workflow.generate_structured_data()
collection.insert_one(data)
```

---

## Troubleshooting

### "No module named 'dotenv'"?

```bash
pip install -r requirements.txt
```

### Mock data instead of real APIs?

Check `.env` file:
- `USE_REAL_APIS=true` is set
- API keys are correct
- Wait 60 seconds (Alpha Vantage rate limits)

### Output files not created?

Make sure the `output/` directory exists:

```bash
mkdir -p output
python main_workflow.py
```

### Unicode/Encoding Errors?

This is normal on some Windows terminals. The workflow still works - the reports are generated correctly.

---

## Cost Estimation

| Service | Free Tier | Cost |
|---------|-----------|------|
| Alpha Vantage | 500/day | Free |
| NewsAPI | 450/day | Free |
| OpenAI | — | ~$0.001/run |
| **Total Monthly** | — | **~$0.03-1.00** |

(Very affordable for daily analysis!)

---

## Next Steps

1. ✅ **Working with mock data** - You have this now
2. 🔜 **Get API keys** - Follow `API_SETUP_GUIDE.md`
3. 🔜 **Enable real APIs** - Update `.env` and set `USE_REAL_APIS=true`
4. 🔜 **Customize stocks** - Edit `config.py`
5. 🔜 **Schedule daily runs** - Set up cron/Task Scheduler
6. 🔜 **Build an Agent** - Next level (autonomous decision-making)

---

## Key Files Reference

| File | Purpose |
|------|---------|
| `config.py` | Customize stocks, APIs, output formats |
| `main_workflow.py` | Run the workflow - start here |
| `stock_data.py` | Fetch stock prices (real or mock) |
| `article_fetcher.py` | Fetch news articles (real or mock) |
| `llm_processor.py` | Process with LLM (real or mock) |
| `output_formatter.py` | Format outputs (TXT, HTML, CSV, JSON) |
| `API_SETUP_GUIDE.md` | How to get and configure API keys |

---

## Summary

You now have a **complete, production-ready workflow** that:

✅ Works out-of-the-box with mock data
✅ Scales to unlimited stocks
✅ Generates professional reports in multiple formats
✅ Can use real APIs when configured
✅ Is easy to customize and extend

**To start:** `python main_workflow.py`

**To use real data:** Follow `API_SETUP_GUIDE.md`

**Questions?** Check the code comments - they explain everything!
