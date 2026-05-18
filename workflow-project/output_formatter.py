"""
Output Formatters for Stock Analysis Workflow
Supports multiple output formats: TXT, JSON, HTML, CSV
"""

import json
from datetime import datetime

class OutputFormatter:
    """Handles all output format generation."""
    
    def __init__(self, results):
        self.results = results
        self.timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    def generate_text_report(self):
        report = f"STOCK ANALYSIS REPORT\nGenerated: {self.timestamp}\n"
        report += "=" * 70 + "\n\n"
        
        for ticker, data in self.results.items():
            stock = data['stock_data']
            report += f"TICKER: {ticker}\n" + "-" * 70 + "\n"
            report += f"Current Price: ${stock['current_price']}\n"
            report += f"Change: {stock['change_percent']}%\n"
            report += f"Trend: {stock['trend'].upper()}\n"
            report += f"Data Source: {stock.get('data_source', 'Unknown')}\n\n"
            report += f"SUMMARY:\n{data['summary']}\n\n"
            sentiment = data['sentiment']
            report += f"SENTIMENT: {sentiment['overall_sentiment'].upper()}\n\n"
            report += "INSIGHTS:\n"
            for i, insight in enumerate(data['insights'], 1):
                report += f"{i}. {insight}\n"
            report += "\n" + "=" * 70 + "\n\n"
        
        return report
    
    def generate_html_report(self):
        html = f"<!DOCTYPE html>\n<html>\n<head>\n<meta charset='UTF-8'>\n"
        html += "<title>Stock Report</title>\n"
        html += "<style>body{{font-family:Arial;margin:20px;background:#f5f5f5}}"
        html += ".container{{max-width:1000px;margin:0 auto;background:white;padding:30px;border-radius:8px;}}"
        html += "h1{{color:#333;border-bottom:3px solid #007bff;}}.stock{{margin:30px 0;padding:20px;border-left:4px solid #007bff;}}"
        html += ".metrics{{display:grid;grid-template-columns:repeat(4,1fr);gap:15px;margin:15px 0;}}"
        html += ".metric{{background:#f9f9f9;padding:12px;border-radius:4px;text-align:center;}}"
        html += ".metric-label{{font-size:0.8em;color:#999;text-transform:uppercase;}}"
        html += ".metric-value{{font-size:1.3em;font-weight:bold;margin-top:5px;}}"
        html += "</style>\n</head>\n<body>\n<div class='container'>\n"
        html += f"<h1>Stock Analysis Report</h1>\n<p>Generated: {self.timestamp}</p>\n"
        
        for ticker, data in self.results.items():
            stock = data['stock_data']
            sentiment = data['sentiment']
            html += f"<div class='stock'>\n<h2>{ticker}</h2>\n"
            html += f"<div class='metrics'>\n"
            html += f"<div class='metric'><div class='metric-label'>Price</div><div class='metric-value'>${stock['current_price']}</div></div>\n"
            html += f"<div class='metric'><div class='metric-label'>Change</div><div class='metric-value'>{stock['change_percent']}%</div></div>\n"
            html += f"<div class='metric'><div class='metric-label'>Trend</div><div class='metric-value'>{stock['trend']}</div></div>\n"
            html += f"<div class='metric'><div class='metric-label'>Sentiment</div><div class='metric-value'>{sentiment['overall_sentiment']}</div></div>\n"
            html += f"</div>\n<p>{data['summary']}</p>\n"
            html += "<ul>\n"
            for insight in data['insights']:
                html += f"<li>{insight}</li>\n"
            html += "</ul>\n</div>\n"
        
        html += "</div>\n</body>\n</html>"
        return html
    
    def generate_csv_report(self):
        csv_data = "Ticker,Price,Change %,Trend,Sentiment\n"
        for ticker, data in self.results.items():
            stock = data['stock_data']
            sentiment = data['sentiment']
            csv_data += f"{ticker},${stock['current_price']},{stock['change_percent']}%,{stock['trend']},{sentiment['overall_sentiment']}\n"
        return csv_data
    
    def save_all_formats(self, output_dir="./output"):
        import os
        os.makedirs(output_dir, exist_ok=True)
        saved_files = []
        
        try:
            text_path = os.path.join(output_dir, "report.txt")
            with open(text_path, 'w') as f:
                f.write(self.generate_text_report())
            print("[OK] Text report saved")
            saved_files.append(text_path)
        except Exception as e:
            print(f"[ERROR] Text: {e}")
        
        try:
            html_path = os.path.join(output_dir, "report.html")
            with open(html_path, 'w') as f:
                f.write(self.generate_html_report())
            print("[OK] HTML report saved")
            saved_files.append(html_path)
        except Exception as e:
            print(f"[ERROR] HTML: {e}")
        
        try:
            csv_path = os.path.join(output_dir, "stocks.csv")
            with open(csv_path, 'w') as f:
                f.write(self.generate_csv_report())
            print("[OK] CSV report saved")
            saved_files.append(csv_path)
        except Exception as e:
            print(f"[ERROR] CSV: {e}")
        
        try:
            data = {"generated": self.timestamp, "stocks": {}}
            for ticker, info in self.results.items():
                data["stocks"][ticker] = {
                    "price": info['stock_data']['current_price'],
                    "trend": info['stock_data']['trend'],
                    "insights": info['insights']
                }
            json_path = os.path.join(output_dir, "data.json")
            with open(json_path, 'w') as f:
                json.dump(data, f, indent=2)
            print("[OK] JSON data saved")
            saved_files.append(json_path)
        except Exception as e:
            print(f"[ERROR] JSON: {e}")

        return saved_files
