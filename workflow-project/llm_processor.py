"""
Steps 3-5: LLM Processing (Summarization, Sentiment Analysis, Report Generation)
This module uses LangChain to process articles and generate insights.
"""

import json
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# For testing without API keys, we provide mock responses
USE_MOCK_LLM = os.getenv("USE_MOCK_LLM", "true").lower() == "true"

if not USE_MOCK_LLM:
    try:
        from langchain.llms import OpenAI
        from langchain.prompts import PromptTemplate
        from langchain.chains import LLMChain
        LANGCHAIN_AVAILABLE = True
    except ImportError:
        LANGCHAIN_AVAILABLE = False
else:
    LANGCHAIN_AVAILABLE = False


class MockLLM:
    """Mock LLM for testing without API keys."""
    
    @staticmethod
    def summarize_articles(articles_text: str) -> str:
        return """
        SUMMARY:
        The articles discuss recent developments in the tech sector. Multiple sources 
        report strong earnings and positive analyst ratings. Market sentiment appears 
        bullish despite some volatility. Key themes include product innovation, 
        market expansion, and competitive positioning.
        """
    
    @staticmethod
    def analyze_sentiment(articles_text: str) -> dict:
        return {
            "overall_sentiment": "positive",
            "positive_articles": 2,
            "neutral_articles": 1,
            "negative_articles": 0,
            "confidence": 0.85,
            "key_sentiment_drivers": [
                "Strong earnings reports",
                "Positive analyst upgrades",
                "New product launches"
            ]
        }
    
    @staticmethod
    def generate_insights(stock_data: dict, articles_text: str, sentiment: dict) -> list:
        return [
            f"The stock is in an {stock_data['trend']} trend with {stock_data['volatility']} volatility",
            f"Recent articles show {sentiment['overall_sentiment']} sentiment",
            "Market analysts are optimistic about future performance",
            "Price momentum appears favorable for near-term trading"
        ]

    @staticmethod
    def decide_action(stock_data: dict, summary: str, sentiment: dict, articles_text: str) -> dict:
        trend = stock_data.get("trend", "neutral").lower()
        volatility = stock_data.get("volatility", "medium").lower()
        sentiment_label = sentiment.get("overall_sentiment", "neutral").lower()

        score = 0
        if trend == "up":
            score += 1
        elif trend == "down":
            score -= 1

        if sentiment_label == "positive":
            score += 1
        elif sentiment_label == "negative":
            score -= 1

        if volatility == "high":
            score -= 1
        elif volatility == "low":
            score += 1

        if score >= 2:
            recommendation = "buy"
        elif score == 1:
            recommendation = "accumulate"
        elif score == 0:
            recommendation = "hold"
        elif score == -1:
            recommendation = "watch"
        else:
            recommendation = "reduce"

        evidence_gaps = []
        if sentiment.get("confidence", 0) < 0.75:
            evidence_gaps.append("Sentiment confidence is below the preferred threshold")
        if volatility == "high":
            evidence_gaps.append("Price volatility is elevated")

        return {
            "recommendation": recommendation,
            "confidence": round(max(0.35, min(0.95, 0.55 + (score * 0.12))), 2),
            "need_more_data": bool(evidence_gaps),
            "evidence_gaps": evidence_gaps,
            "rationale": [
                f"Trend signal is {trend}",
                f"Sentiment is {sentiment_label}",
                f"Volatility is {volatility}",
            ],
            "next_actions": [
                "Monitor the next news cycle",
                "Recheck price action if new catalysts appear",
            ],
            "summary": summary.strip(),
        }

    @staticmethod
    def plan_next_actions(ticker: str, state: dict, run_memory: dict) -> dict:
        article_count = state.get("article_count", 0)
        summary_ready = bool(state.get("summary"))
        sentiment = state.get("sentiment", {}) or {}
        decision = state.get("decision", {}) or {}
        stock_data = state.get("stock_data", {}) or {}
        lessons = run_memory.get("lessons", []) if run_memory else []

        steps = []
        requery = {"needed": False, "tool": "fetch_articles", "arguments": {}, "reason": ""}
        memory_updates = []

        if article_count == 0:
            steps.extend([
                {"tool": "fetch_articles", "arguments": {"count": 3}, "reason": "Bootstrap the analysis with current articles"},
                {"tool": "format_articles", "arguments": {}, "reason": "Prepare articles for the LLM"},
                {"tool": "summarize_articles", "arguments": {}, "reason": "Condense the evidence"},
                {"tool": "analyze_sentiment", "arguments": {}, "reason": "Score the tone of the articles"},
                {"tool": "generate_insights", "arguments": {}, "reason": "Convert evidence into trade ideas"},
                {"tool": "decide_action", "arguments": {}, "reason": "Choose the final action"},
            ])
        else:
            if not summary_ready:
                steps.append({"tool": "summarize_articles", "arguments": {}, "reason": "A summary is still missing"})
            if not sentiment:
                steps.append({"tool": "analyze_sentiment", "arguments": {}, "reason": "Sentiment has not been computed yet"})
            if not state.get("insights"):
                steps.append({"tool": "generate_insights", "arguments": {}, "reason": "Need actionable observations"})
            if not decision:
                steps.append({"tool": "decide_action", "arguments": {}, "reason": "Need a recommendation before stopping"})

        confidence = float(sentiment.get("confidence", 0) or 0)
        decision_confidence = float(decision.get("confidence", 0) or 0)
        volatility = stock_data.get("volatility", "medium")

        if article_count > 0 and (
            confidence < 0.75
            or decision.get("need_more_data")
            or decision_confidence < 0.78
            or volatility == "high"
        ):
            requery = {
                "needed": True,
                "tool": "fetch_articles",
                "arguments": {"count": 5},
                "reason": "The current evidence is not strong enough to stop yet",
            }
            memory_updates.append(
                f"{ticker}: re-query recommended because confidence={confidence:.2f}, decision={decision_confidence:.2f}, volatility={volatility}"
            )

        stop = bool(decision) and decision_confidence >= 0.78 and not decision.get("need_more_data") and not requery["needed"]

        if lessons:
            memory_updates.append(f"Prior lessons considered: {len(lessons)}")

        return {
            "objective": f"Build an evidence-based recommendation for {ticker}",
            "state_summary": {
                "article_count": article_count,
                "summary_ready": summary_ready,
                "sentiment_confidence": confidence,
                "decision_confidence": decision_confidence,
                "volatility": volatility,
            },
            "steps": steps,
            "requery": requery,
            "stop": stop,
            "memory_updates": memory_updates,
            "reasoning": [
                f"Trend is {stock_data.get('trend', 'unknown')}",
                f"Sentiment confidence is {confidence:.2f}",
                f"Decision confidence is {decision_confidence:.2f}",
            ],
        }


class LLMProcessor:
    """Processes articles using LLM (or mock for testing)."""
    
    def __init__(self):
        self.use_mock = USE_MOCK_LLM or not LANGCHAIN_AVAILABLE
        
        if not self.use_mock:
            api_key = os.getenv("OPENAI_API_KEY")
            if not api_key:
                print("⚠️  No OPENAI_API_KEY found. Switching to mock mode.")
                self.use_mock = True
            else:
                self.llm = OpenAI(temperature=0.3, max_tokens=500)
    
    def summarize_articles(self, articles_text: str) -> str:
        """Step 3: Summarize articles."""
        if self.use_mock:
            return MockLLM.summarize_articles(articles_text)
        
        # Real LLM call
        prompt = PromptTemplate(
            input_variables=["articles"],
            template="Please provide a concise summary of the following articles:\n\n{articles}"
        )
        chain = LLMChain(llm=self.llm, prompt=prompt)
        return chain.run(articles=articles_text)
    
    def analyze_sentiment(self, articles_text: str) -> dict:
        """Step 4: Analyze sentiment of articles."""
        if self.use_mock:
            return MockLLM.analyze_sentiment(articles_text)
        
        # Real LLM call
        prompt = PromptTemplate(
            input_variables=["articles"],
            template="""Analyze the sentiment of these articles. Respond in JSON format:
{
    "overall_sentiment": "positive/negative/neutral",
    "positive_articles": <count>,
    "neutral_articles": <count>,
    "negative_articles": <count>,
    "confidence": <0-1>,
    "key_sentiment_drivers": [<list of reasons>]
}

Articles:
{articles}"""
        )
        chain = LLMChain(llm=self.llm, prompt=prompt)
        response = chain.run(articles=articles_text)
        
        # Parse JSON response (simplified)
        import json
        try:
            return json.loads(response)
        except:
            return MockLLM.analyze_sentiment(articles_text)
    
    def generate_insights(self, stock_data: dict, articles_text: str, sentiment: dict) -> list:
        """Step 5: Generate actionable insights."""
        if self.use_mock:
            return MockLLM.generate_insights(stock_data, articles_text, sentiment)
        
        # Real LLM call
        prompt = PromptTemplate(
            input_variables=["stock_trend", "sentiment", "articles"],
            template="""Based on the following data, provide 3-4 key investment insights:
Stock Trend: {stock_trend}
Market Sentiment: {sentiment}
Articles: {articles}

Format as a numbered list."""
        )
        chain = LLMChain(llm=self.llm, prompt=prompt)
        response = chain.run(
            stock_trend=f"{stock_data['trend']} ({stock_data['change_percent']}%)",
            sentiment=sentiment['overall_sentiment'],
            articles=articles_text
        )
        
        # Parse response into list
        return [line.strip() for line in response.split('\n') if line.strip() and line[0].isdigit()]

    def plan_next_actions(self, ticker: str, state: dict, run_memory: dict) -> dict:
        """Agent step: create the next tool plan from the current state."""
        if self.use_mock:
            return MockLLM.plan_next_actions(ticker, state, run_memory)

        prompt = PromptTemplate(
            input_variables=["ticker", "state", "run_memory"],
            template="""You are the planning module of an autonomous stock analysis agent.
Choose the next tools to call and whether the agent should re-query for more evidence.

Available tools:
- fetch_stock_snapshot
- fetch_articles
- format_articles
- summarize_articles
- analyze_sentiment
- generate_insights
- decide_action

Return JSON only in this format:
{
  "objective": "...",
  "state_summary": {"article_count": 0, "summary_ready": false, "sentiment_confidence": 0.0, "decision_confidence": 0.0, "volatility": "low"},
  "steps": [
    {"tool": "fetch_articles", "arguments": {"count": 3}, "reason": "..."}
  ],
  "requery": {"needed": true, "tool": "fetch_articles", "arguments": {"count": 5}, "reason": "..."},
  "stop": false,
  "memory_updates": ["..."],
  "reasoning": ["..."]
}

Ticker: {ticker}
State: {state}
Run memory: {run_memory}"""
        )
        chain = LLMChain(llm=self.llm, prompt=prompt)
        response = chain.run(
            ticker=ticker,
            state=json.dumps(state, indent=2),
            run_memory=json.dumps(run_memory, indent=2),
        )

        try:
            return json.loads(response)
        except json.JSONDecodeError:
            return MockLLM.plan_next_actions(ticker, state, run_memory)

    def decide_action(self, stock_data: dict, summary: str, sentiment: dict, articles_text: str) -> dict:
        """Agent step: decide what action to take based on the evidence."""
        if self.use_mock:
            return MockLLM.decide_action(stock_data, summary, sentiment, articles_text)

        prompt = PromptTemplate(
            input_variables=["stock_data", "summary", "sentiment", "articles"],
            template="""You are an autonomous stock analysis agent.
Given the evidence below, decide the most prudent action.

Return JSON only in this format:
{
  "recommendation": "buy|accumulate|hold|watch|reduce",
  "confidence": 0.0,
  "need_more_data": true,
  "evidence_gaps": ["..."],
  "rationale": ["..."],
  "next_actions": ["..."],
  "summary": "..."
}

Stock data: {stock_data}
Summary: {summary}
Sentiment: {sentiment}
Articles: {articles}"""
        )
        chain = LLMChain(llm=self.llm, prompt=prompt)
        response = chain.run(
            stock_data=json.dumps(stock_data, indent=2),
            summary=summary,
            sentiment=json.dumps(sentiment, indent=2),
            articles=articles_text,
        )

        try:
            return json.loads(response)
        except json.JSONDecodeError:
            return MockLLM.decide_action(stock_data, summary, sentiment, articles_text)


if __name__ == "__main__":
    # Test the module
    processor = LLMProcessor()
    sample_articles = "Article about company growth and new product launches..."
    
    print("Testing LLM Processor (Mock Mode):\n")
    print("SUMMARY:")
    print(processor.summarize_articles(sample_articles))
    
    print("\nSENTIMENT ANALYSIS:")
    print(processor.analyze_sentiment(sample_articles))
    
    sample_stock = {"trend": "up", "change_percent": 2.5}
    print("\nINSIGHTS:")
    for insight in processor.generate_insights(sample_stock, sample_articles, {"overall_sentiment": "positive"}):
        print(f"  • {insight}")
