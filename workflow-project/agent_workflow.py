"""
Autonomous stock analysis agent.
This mode keeps the existing data fetchers but adds a decision loop that can
request more evidence before producing a recommendation.
"""

import json
from datetime import datetime

from article_fetcher import get_stock_articles, format_articles_for_processing
from config import get_selected_stocks, print_config
from llm_processor import LLMProcessor
from output_formatter import OutputFormatter
from stock_data import get_multiple_stocks


class StockAnalysisAgent:
    """Agentic version of the stock analysis workflow."""

    def __init__(self, stocks: list = None, max_iterations: int = 2, confidence_threshold: float = 0.75):
        if stocks is None:
            stocks = get_selected_stocks()

        self.stocks = stocks
        self.max_iterations = max_iterations
        self.confidence_threshold = confidence_threshold
        self.results = {}
        self.processor = LLMProcessor()

    def run(self):
        """Execute the autonomous analysis loop."""
        print("=" * 60)
        print("AUTONOMOUS STOCK ANALYSIS AGENT STARTED")
        print("=" * 60)
        print(f"Target stocks: {', '.join(self.stocks)}")
        print(f"Confidence threshold: {self.confidence_threshold}")
        print()

        stock_data = get_multiple_stocks(self.stocks)

        for ticker in self.stocks:
            print(f"\nAgent analyzing {ticker}...")
            print("-" * 40)

            evidence_log = []
            articles = get_stock_articles(ticker, count=3)
            articles_text = format_articles_for_processing(articles)
            evidence_log.append(f"Fetched {len(articles)} baseline articles")

            analysis = self._analyze_evidence(ticker, stock_data[ticker], articles, articles_text)

            iteration = 1
            while iteration < self.max_iterations and analysis["decision"]["need_more_data"]:
                evidence_log.append("Decision requested more data, fetching additional articles")
                extra_articles = get_stock_articles(ticker, count=5)
                articles = self._merge_articles(articles, extra_articles)
                articles_text = format_articles_for_processing(articles)
                analysis = self._analyze_evidence(ticker, stock_data[ticker], articles, articles_text)
                iteration += 1

            analysis["agent_trace"] = evidence_log
            analysis["analysis_iterations"] = iteration
            self.results[ticker] = analysis

        print("\n" + "=" * 60)
        print("AGENT ANALYSIS COMPLETED")
        print("=" * 60)

        return self.results

    def _merge_articles(self, primary_articles: list, secondary_articles: list) -> list:
        seen = set()
        merged = []

        for article in primary_articles + secondary_articles:
            key = (article.get("title", ""), article.get("published_at", ""))
            if key in seen:
                continue
            seen.add(key)
            merged.append(article)

        return merged

    def _analyze_evidence(self, ticker: str, stock_data: dict, articles: list, articles_text: str) -> dict:
        print("  STEP 1: Summarizing evidence...")
        summary = self.processor.summarize_articles(articles_text)
        print("  [OK] Summary generated")

        print("  STEP 2: Assessing sentiment...")
        sentiment = self.processor.analyze_sentiment(articles_text)
        print(f"  [OK] Sentiment: {sentiment['overall_sentiment'].upper()}")

        print("  STEP 3: Generating insights...")
        insights = self.processor.generate_insights(stock_data, articles_text, sentiment)
        print("  [OK] Insights generated")

        print("  STEP 4: Making decision...")
        decision = self.processor.decide_action(stock_data, summary, sentiment, articles_text)
        print(f"  [OK] Recommendation: {decision['recommendation'].upper()} (confidence {decision['confidence']})")

        return {
            "stock_data": stock_data,
            "articles": articles,
            "summary": summary,
            "sentiment": sentiment,
            "insights": insights,
            "decision": decision,
            "ticker": ticker,
            "generated_at": datetime.now().isoformat(),
        }

    def generate_report(self) -> str:
        """Generate an agent-oriented report from results."""
        report = f"AUTONOMOUS STOCK ANALYSIS REPORT\n"
        report += f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        report += "=" * 60 + "\n\n"

        for ticker, data in self.results.items():
            stock = data["stock_data"]
            decision = data["decision"]

            report += f"TICKER: {ticker}\n"
            report += "-" * 40 + "\n"
            report += f"Current Price: ${stock['current_price']}\n"
            report += f"Trend: {stock['trend'].upper()}\n"
            report += f"Volatility: {stock['volatility']}\n"
            report += f"Decision: {decision['recommendation'].upper()}\n"
            report += f"Confidence: {decision['confidence']}\n"
            report += f"Need More Data: {decision['need_more_data']}\n\n"

            report += "RATIONALE:\n"
            for i, item in enumerate(decision.get("rationale", []), 1):
                report += f"{i}. {item}\n"

            if decision.get("evidence_gaps"):
                report += "\nEVIDENCE GAPS:\n"
                for gap in decision["evidence_gaps"]:
                    report += f"- {gap}\n"

            report += "\nKEY INSIGHTS:\n"
            for i, insight in enumerate(data["insights"], 1):
                report += f"{i}. {insight}\n"

            report += "\n" + "=" * 60 + "\n\n"

        return report

    def save_outputs(self, output_dir: str = "./output"):
        """Save the agent outputs using the shared formatter."""
        import os

        os.makedirs(output_dir, exist_ok=True)

        formatter = OutputFormatter(self.results)
        saved_files = formatter.save_all_formats(output_dir)

        agent_report_path = os.path.join(output_dir, "agent_report.txt")
        with open(agent_report_path, "w", encoding="utf-8") as file_handle:
            file_handle.write(self.generate_report())
        saved_files.append(agent_report_path)

        agent_json_path = os.path.join(output_dir, "agent_data.json")
        with open(agent_json_path, "w", encoding="utf-8") as file_handle:
            json.dump({"generated_at": datetime.now().isoformat(), "stocks": self.results}, file_handle, indent=2, default=str)
        saved_files.append(agent_json_path)

        print(f"[OK] Agent outputs saved to {output_dir}")
        print(f"  Files: {len(saved_files)} generated")


def main():
    """Run the autonomous agent from the command line."""
    print_config()
    agent = StockAnalysisAgent()
    agent.run()

    print("\n" + "=" * 60)
    print("AGENT OUTPUT")
    print("=" * 60 + "\n")
    print(agent.generate_report())

    print("\nSaving agent outputs in multiple formats...")
    agent.save_outputs("./output")
    print("[OK] Agent run complete!\n")


if __name__ == "__main__":
    main()
