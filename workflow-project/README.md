# Stock Analysis Workflow Project

## Overview

This project demonstrates a **real workflow** - a predefined sequence of steps that retrieves stock data, fetches articles, summarizes them, analyzes sentiment, and generates insights.

### What Makes This a Workflow?

✅ **Predefined Steps** - The sequence is fixed: Data → Articles → Summary → Sentiment → Insights  
✅ **Human-Controlled Path** - You decide what stocks, what articles, what output format  
✅ **LLM as Executor** - The LLM follows instructions, doesn't make decisions  
✅ **Deterministic Flow** - Same input = Same output (within reason)  

**This is NOT an Agent because:** The LLM doesn't decide which tools to use or what to do. The workflow decides everything.

---

## Project Structure

```
workflow-project/
├── main_workflow.py        # Main orchestrator (runs all steps)
├── stock_data.py           # Step 1: Retrieve stock data
├── article_fetcher.py      # Step 2: Fetch articles
├── llm_processor.py        # Steps 3-5: LLM processing
├── requirements.txt        # Python dependencies
├── .env.example           # Environment variables template
└── README.md              # This file
```

---

## Quick Start

### 1. Install Dependencies

```bash
cd workflow-project
pip install -r requirements.txt
```

### 2. Set Up Environment Variables (Optional)

```bash
cp .env.example .env
```

Then add your OpenAI API key to `.env`:
```
OPENAI_API_KEY=sk-...
USE_MOCK_LLM=false
```

**Note:** Without an API key, the workflow will use mock responses. This is perfect for testing!

### 3. Run the Workflow

```bash
python main_workflow.py
```

You should see output like:
```
============================================================
STOCK ANALYSIS WORKFLOW STARTED
============================================================
Processing stocks: AAPL, MSFT

STEP 1: Retrieving stock data...
✓ Stock data retrieved

Processing AAPL...
  STEP 2: Fetching articles...
  ✓ Fetched 3 articles
  
  STEP 3: Summarizing articles with LLM...
  ✓ Summary generated
  ...
```

### 4. View Results

Three output files are created in `./output/`:

- **report.txt** - Human-readable summary
- **data.json** - Structured data (easy to parse programmatically)
- **results.json** - Complete results with all details

---

## Understanding the Workflow

### The 5-Step Process

#### Step 1: Retrieve Stock Data
```python
stock_data = get_stock_data("AAPL")
# Returns: {
#   "ticker": "AAPL",
#   "current_price": 175.43,
#   "trend": "up",
#   "change_percent": 2.5,
#   "volatility": "low"
# }
```

#### Step 2: Fetch Articles
```python
articles = get_stock_articles("AAPL", count=3)
# Returns: List of article dicts with title, source, description, etc.
```

#### Step 3: Summarize (LLM)
```python
summary = processor.summarize_articles(articles_text)
# LLM generates: "The articles discuss recent developments..."
```

#### Step 4: Analyze Sentiment (LLM)
```python
sentiment = processor.analyze_sentiment(articles_text)
# LLM returns: {
#   "overall_sentiment": "positive",
#   "positive_articles": 2,
#   "negative_articles": 0,
#   "confidence": 0.85
# }
```

#### Step 5: Generate Insights (LLM)
```python
insights = processor.generate_insights(stock_data, articles_text, sentiment)
# LLM returns: ["Insight 1", "Insight 2", "Insight 3"]
```

---

## Customization

### Add More Stocks

Edit `main_workflow.py`:
```python
STOCKS_TO_ANALYZE = ["AAPL", "MSFT", "GOOGL", "TSLA"]
```

### Use Real Data

Replace the mock data functions:
- **Stock Data:** Use [Alpha Vantage](https://www.alphavantage.co/), [IEX Cloud](https://iexcloud.io/), or [Polygon.io](https://polygon.io/)
- **Articles:** Use [NewsAPI](https://newsapi.org/), RSS feeds, or web scraping

Example - Stock Data with Alpha Vantage:
```python
import requests

def get_stock_data(ticker: str) -> dict:
    url = f"https://www.alphavantage.co/query"
    params = {
        "function": "GLOBAL_QUOTE",
        "symbol": ticker,
        "apikey": os.getenv("ALPHAVANTAGE_KEY")
    }
    response = requests.get(url, params=params)
    data = response.json()
    # Parse and return...
```

### Use Real LLM API

Your workflow will automatically use OpenAI if you set:
```
OPENAI_API_KEY=sk-...
USE_MOCK_LLM=false
```

Or use a different LLM like Claude:
```python
from langchain.llms import Anthropic
self.llm = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
```

---

## Key Takeaways

### What Makes This a Workflow?

| Aspect | This Workflow |
|--------|---------------|
| **Steps Defined?** | ✅ Yes - 5 fixed steps |
| **Who Decides the Path?** | ✅ Human (programmer) - not the LLM |
| **Can It Adapt?** | ❌ No - always follows the same path |
| **Is LLM Autonomous?** | ❌ No - follows instructions exactly |
| **Good for Repetitive Tasks?** | ✅ Yes - excellent |

### Next Step: Convert to an Agent

To make this an **Agent**, you would:

1. Give the LLM access to tools (Stock API, News API, Analysis tools)
2. Give it a goal: *"Provide investment analysis for these stocks"*
3. Let it decide: Which tools to use, in what order, whether to iterate
4. Add a reasoning loop: Think → Act → Observe → Repeat

---

## File Explanations

### main_workflow.py
The orchestrator that runs all steps in sequence. This is where the workflow logic lives.

### stock_data.py
Returns simulated stock data. In production, call a real API.

### article_fetcher.py
Returns simulated articles and formats them for LLM processing.

### llm_processor.py
Handles all LLM calls with fallback to mock responses. Easy to swap out for different LLMs.

---

## Troubleshooting

### "No module named 'langchain'"
```bash
pip install -r requirements.txt
```

### "OPENAI_API_KEY not found"
The workflow will automatically use mock responses. This is fine for testing!

### Want to use real OpenAI API?
1. Get an API key from [platform.openai.com](https://platform.openai.com)
2. Create `.env` file with `OPENAI_API_KEY=sk-...`
3. Set `USE_MOCK_LLM=false`

### Output files not created?
Make sure the `./output` directory can be created:
```bash
mkdir output
python main_workflow.py
```

---

## Next Steps

1. ✅ **Run this workflow** - Get it working with mock data
2. 🔄 **Customize it** - Add your own stocks, change the output format
3. 📊 **Add real data** - Connect to real APIs
4. 🚀 **Upgrade to an agent** - Let the LLM make decisions (see next project)

---

## Run the Streamlit Dashboard (UI)

This project includes a Streamlit dashboard (`app.py`) that wraps the workflow and agent features in a polished UI.

1. From the `workflow-project` folder, install dependencies (if not already done):

```bash
cd workflow-project
pip install -r requirements.txt
```

2. Run the Streamlit app (default port 8501):

```bash
python -m streamlit run app.py --server.port 8501 --server.headless true
```

3. Open your browser at `http://127.0.0.1:8501` to view the dashboard. Refresh the page after code changes.

Notes:
- If Streamlit prompts for an email when you run it, you can safely skip account creation — it will still serve the app.
- If the port 8501 is in use, change `--server.port` to another port.
- To run with real LLMs, add your API keys to `.env` and set `USE_MOCK_LLM=false`.


## Resources

- [LangChain Documentation](https://python.langchain.com/)
- [OpenAI API Documentation](https://platform.openai.com/docs)
- [NewsAPI](https://newsapi.org/)
- [Alpha Vantage Stock Data](https://www.alphavantage.co/)

---

**Questions?** Review the code comments - they explain each step!
