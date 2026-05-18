"""
Stock Analysis Workflow - Main Orchestrator
This is the central workflow that connects all steps in sequence.

WORKFLOW STEPS (Predefined & Human-Controlled):
1. Retrieve stock data
2. Fetch related articles
3. Summarize articles with LLM
4. Analyze sentiment with LLM
5. Generate final report with insights
6. Save outputs in multiple formats
"""

import argparse
import json
from datetime import datetime
from config import STOCKS, get_selected_stocks, print_config, OUTPUT_FORMATS
from stock_data import get_stock_data, get_multiple_stocks
from article_fetcher import get_stock_articles, format_articles_for_processing
from llm_processor import LLMProcessor
from output_formatter import OutputFormatter

from agent_tool_driven import StockAnalysisAgent


class StockAnalysisWorkflow:
    """Main workflow orchestrator."""
    
    def __init__(self, stocks: list = None):
        """
        Initialize workflow with stock tickers.
        
        Args:
            stocks: List of stock tickers (e.g., ['AAPL', 'GOOGL'])
                   If None, uses default from config
        """
        if stocks is None:
            stocks = get_selected_stocks()
        
        self.stocks = stocks
        self.results = {}
        self.processor = LLMProcessor()
    
    def run(self):
        """Execute the complete workflow."""
        print("=" * 60)
        print("STOCK ANALYSIS WORKFLOW STARTED")
        print("=" * 60)
        print(f"Processing stocks: {', '.join(self.stocks)}")
        print()
        
        # STEP 1: Retrieve stock data
        print("STEP 1: Retrieving stock data...")
        stock_data = get_multiple_stocks(self.stocks)
        print("✓ Stock data retrieved\n")
        
        # Process each stock
        for ticker in self.stocks:
            print(f"\nProcessing {ticker}...")
            print("-" * 40)
            
            data = stock_data[ticker]
            
            # STEP 2: Fetch articles
            print("  STEP 2: Fetching articles...")
            articles = get_stock_articles(ticker, count=3)
            articles_text = format_articles_for_processing(articles)
            print(f"  ✓ Fetched {len(articles)} articles\n")
            
            # STEP 3: Summarize articles
            print("  STEP 3: Summarizing articles with LLM...")
            summary = self.processor.summarize_articles(articles_text)
            print("  ✓ Summary generated\n")
            
            # STEP 4: Analyze sentiment
            print("  STEP 4: Analyzing sentiment...")
            sentiment = self.processor.analyze_sentiment(articles_text)
            print(f"  ✓ Sentiment analyzed: {sentiment['overall_sentiment'].upper()}\n")
            
            # STEP 5: Generate insights
            print("  STEP 5: Generating insights...")
            insights = self.processor.generate_insights(data, articles_text, sentiment)
            print("  ✓ Insights generated\n")
            
            # Store results
            self.results[ticker] = {
                "stock_data": data,
                "articles": articles,
                "summary": summary,
                "sentiment": sentiment,
                "insights": insights
            }
        
        print("\n" + "=" * 60)
        print("WORKFLOW COMPLETED")
        print("=" * 60)
        
        return self.results
    
    def generate_report(self) -> str:
        """Generate formatted report from results."""
        report = f"STOCK ANALYSIS REPORT\n"
        report += f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        report += "=" * 60 + "\n\n"
        
        for ticker, data in self.results.items():
            stock = data['stock_data']
            
            # Stock Overview
            report += f"TICKER: {ticker}\n"
            report += "-" * 40 + "\n"
            report += f"Current Price: ${stock['current_price']}\n"
            report += f"Previous Close: ${stock['previous_close']}\n"
            report += f"Change: {stock['change_percent']}%\n"
            report += f"Trend: {stock['trend'].upper()}\n"
            report += f"Volatility: {stock['volatility']}\n\n"
            
            # Summary
            report += "SUMMARY:\n"
            report += data['summary'] + "\n\n"
            
            # Sentiment
            report += "SENTIMENT ANALYSIS:\n"
            sentiment = data['sentiment']
            report += f"Overall: {sentiment['overall_sentiment'].upper()} "
            report += f"(Confidence: {sentiment['confidence']})\n"
            report += f"Positive Articles: {sentiment['positive_articles']}\n"
            report += f"Neutral Articles: {sentiment['neutral_articles']}\n"
            report += f"Negative Articles: {sentiment['negative_articles']}\n\n"
            
            # Insights
            report += "KEY INSIGHTS:\n"
            for i, insight in enumerate(data['insights'], 1):
                report += f"{i}. {insight}\n"
            
            report += "\n" + "=" * 60 + "\n\n"
        
        return report
    
    def generate_structured_data(self) -> dict:
        """Generate structured data for programmatic use."""
        structured = {
            "generated_at": datetime.now().isoformat(),
            "stocks": {}
        }
        
        for ticker, data in self.results.items():
            structured["stocks"][ticker] = {
                "price": data['stock_data']['current_price'],
                "trend": data['stock_data']['trend'],
                "change_percent": data['stock_data']['change_percent'],
                "sentiment": data['sentiment']['overall_sentiment'],
                "sentiment_confidence": data['sentiment']['confidence'],
                "article_count": len(data['articles']),
                "insights": data['insights']
            }
        
        return structured
    
    def save_outputs(self, output_dir: str = "./output"):
        """
        Save all outputs to files using OutputFormatter.
        
        Args:
            output_dir: Directory to save outputs
        """
        import os
        os.makedirs(output_dir, exist_ok=True)
        
        # Use OutputFormatter for all formats
        formatter = OutputFormatter(self.results)
        saved_files = formatter.save_all_formats(output_dir)
        
        print(f"✓ All outputs saved to {output_dir}")
        print(f"  Files: {len(saved_files)} generated")


def main():
    """Main entry point - demonstrates the workflow or the agent mode."""
    parser = argparse.ArgumentParser(description="Stock analysis workflow")
    parser.add_argument(
        "--agent",
        action="store_true",
        help="Run the autonomous agent version instead of the fixed workflow",
    )
    parser.add_argument(
        "--stocks",
        nargs="+",
        help="Optional list of tickers to analyze",
    )
    args = parser.parse_args()
    
    # Show configuration
    print_config()

    if args.agent:
        print("Running in agent mode...\n")
        runner = StockAnalysisAgent(stocks=args.stocks)
        runner.run()

        print("\n" + "=" * 60)
        print("AGENT OUTPUT")
        print("=" * 60 + "\n")
        print(runner.generate_report())

        print("\nSaving outputs in multiple formats...")
        runner.save_outputs("./output")
        print("✓ Agent outputs saved!\n")
        return
    
    # Run the workflow with stocks from config
    workflow = StockAnalysisWorkflow(stocks=args.stocks)
    workflow.run()
    
    # Display results
    print("\n" + "=" * 60)
    print("WORKFLOW OUTPUT")
    print("=" * 60 + "\n")
    print(workflow.generate_report())
    
    # Save outputs in all formats
    print("\nSaving outputs in multiple formats...")
    workflow.save_outputs("./output")
    print("✓ All outputs saved!\n")


if __name__ == "__main__":
    main()
