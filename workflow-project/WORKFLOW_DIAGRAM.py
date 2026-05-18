"""
Visual Workflow Diagram
Shows the exact flow of the stock analysis workflow.
"""

WORKFLOW_DIAGRAM = """
╔════════════════════════════════════════════════════════════════════╗
║              STOCK ANALYSIS WORKFLOW - VISUAL FLOW                 ║
╚════════════════════════════════════════════════════════════════════╝

USER INPUT: Select stocks ["AAPL", "MSFT"]
    │
    ▼
┌────────────────────────────────────────────────────────────────┐
│ STEP 1: RETRIEVE STOCK DATA (stock_data.py)                   │
├────────────────────────────────────────────────────────────────┤
│ Input:  Ticker symbol (e.g., "AAPL")                          │
│ Action: Fetch current price, trend, volatility                │
│ Output: {                                                       │
│           "current_price": 175.43,                             │
│           "trend": "up",                                        │
│           "change_percent": 2.5,                               │
│           ...                                                   │
│         }                                                       │
└────────────────────────────────────────────────────────────────┘
    │
    ▼
┌────────────────────────────────────────────────────────────────┐
│ STEP 2: FETCH ARTICLES (article_fetcher.py)                   │
├────────────────────────────────────────────────────────────────┤
│ Input:  Ticker symbol                                         │
│ Action: Fetch news articles about the stock                   │
│ Output: [                                                       │
│           {                                                     │
│             "title": "AAPL Surges After Earnings",             │
│             "source": "Bloomberg",                             │
│             "description": "...",                              │
│           },                                                    │
│           ...                                                   │
│         ]                                                       │
└────────────────────────────────────────────────────────────────┘
    │
    ▼
┌────────────────────────────────────────────────────────────────┐
│ STEP 3: SUMMARIZE (llm_processor.py → LLM)                    │
├────────────────────────────────────────────────────────────────┤
│ Input:  Raw article text                                      │
│ Action: Send to LLM: "Summarize these articles"               │
│ Output: "The articles discuss recent developments in the       │
│          tech sector. Strong earnings were reported..."        │
└────────────────────────────────────────────────────────────────┘
    │
    ▼
┌────────────────────────────────────────────────────────────────┐
│ STEP 4: ANALYZE SENTIMENT (llm_processor.py → LLM)            │
├────────────────────────────────────────────────────────────────┤
│ Input:  Raw article text                                      │
│ Action: Send to LLM: "What's the sentiment of these?"         │
│ Output: {                                                       │
│           "overall_sentiment": "positive",                     │
│           "positive_articles": 2,                              │
│           "negative_articles": 0,                              │
│           "confidence": 0.85                                    │
│         }                                                       │
└────────────────────────────────────────────────────────────────┘
    │
    ▼
┌────────────────────────────────────────────────────────────────┐
│ STEP 5: GENERATE INSIGHTS (llm_processor.py → LLM)            │
├────────────────────────────────────────────────────────────────┤
│ Input:  Stock data + articles + sentiment                     │
│ Action: Send to LLM: "Generate investment insights"           │
│ Output: [                                                       │
│           "Stock in uptrend with positive sentiment",          │
│           "Recent earnings exceeded expectations",             │
│           "Analyst upgrades support bullish outlook"           │
│         ]                                                       │
└────────────────────────────────────────────────────────────────┘
    │
    ▼
┌────────────────────────────────────────────────────────────────┐
│ STEP 6: COMPILE & SAVE OUTPUTS                                │
├────────────────────────────────────────────────────────────────┤
│ Output 1: report.txt         (Human-readable summary)         │
│ Output 2: data.json          (Structured data)                │
│ Output 3: results.json       (Complete results)               │
└────────────────────────────────────────────────────────────────┘
    │
    ▼
    WORKFLOW COMPLETE ✓


KEY CHARACTERISTICS OF THIS WORKFLOW:
════════════════════════════════════════

✓ STEPS ARE PREDEFINED        → Always: 1 → 2 → 3 → 4 → 5 → 6
✓ PATH IS FIXED              → No branching, no loops, no decisions
✓ HUMAN CONTROLS THE FLOW    → Human decides: which stocks, what to output
✓ LLM EXECUTES INSTRUCTIONS  → LLM doesn't choose which tool to use
✓ DETERMINISTIC OUTPUT       → Same input produces consistent output
✓ SCALES EASILY              → Add 100 stocks? Just loop the process


COMPARISON: WORKFLOW vs AGENT
═════════════════════════════════════════════════════════════════

WHAT MAKES THIS A WORKFLOW:
  
    Goal: "Run stock analysis in a fixed, repeatable sequence"
  
    FLOW:
        ├─ Retrieve stock data
        ├─ Fetch related articles
        ├─ Summarize articles
        ├─ Analyze sentiment
        ├─ Generate insights
        └─ Save outputs

    THE WORKFLOW RULES:
        • Steps are predefined
        • The path is fixed
        • The human chooses inputs and mode
        • The LLM executes prompts, not strategy
        • Output is deterministic for the same inputs


WHAT MAKES THIS AN AI AGENT:

    Goal: "Analyze these stocks and decide what to do next"

    AGENT BEHAVIOR:
        ├─ Creates an explicit plan before acting
        ├─ Chooses which tools to call next
        ├─ Re-queries for more evidence when confidence is weak
        ├─ Invalidates stale analysis after new data arrives
        ├─ Stores run memory and lessons across executions
        └─ Stops when the evidence is strong enough

    THE DIFFERENCE:
        • The agent decides the next step, not the user
        • The agent can loop, revise, and re-plan
        • The agent can carry memory across runs
        • The agent adapts to weaker or surprising evidence
        • It is more expensive and slower, but more flexible


CURRENT WORKFLOW ADVANTAGES:
═════════════════════════════════════════════════════════════════

✓ Cheaper (fewer LLM calls needed)
✓ Faster (no thinking/reasoning overhead)
✓ Predictable (same result every time)
✓ Debuggable (you know exactly what happens)
✓ Perfect for repetitive tasks


WHEN TO UPGRADE TO AN AGENT:
═════════════════════════════════════════════════════════════════

✅ You need explicit planning
✅ You need re-querying and self-correction
✅ You want memory across runs
✅ You want the system to decide what to do next
✓ Then: Use the agent version
"""

if __name__ == "__main__":
    print(WORKFLOW_DIAGRAM)
