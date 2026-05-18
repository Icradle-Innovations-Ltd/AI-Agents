import json
import traceback
from main_workflow import StockAnalysisWorkflow
from output_formatter import OutputFormatter

try:
    print("Initializing workflow with AAPL...")
    workflow = StockAnalysisWorkflow(stocks=["AAPL"])
    print("Running workflow...")
    workflow.run()

    print("\nResults structure:")
    structure = {k: list(v.keys()) for k, v in workflow.results.items()}
    print(json.dumps(structure, indent=2))

    # Try generating HTML
    try:
        print("\nAttempting HTML generation...")
        formatter = OutputFormatter(workflow.results)
        html = formatter.generate_html_report()
        if html:
            print(f"HTML generated successfully: {len(html)} chars")
            with open("debug_report.html", "w", encoding="utf-8") as f:
                f.write(html)
            print("Report saved to debug_report.html")
        else:
            print("HTML generation returned empty string.")
    except Exception as e:
        print(f"\nHTML Error: {e}")
        traceback.print_exc()

except Exception as e:
    print(f"\nWorkflow execution failed: {e}")
    traceback.print_exc()
