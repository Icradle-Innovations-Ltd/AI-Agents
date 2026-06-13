"""
Autonomous stock analysis agent with explicit planning, re-querying,
and a richer memory/state loop.
"""

import json
import os
from datetime import datetime

from article_fetcher import format_articles_for_processing, get_stock_articles
from config import get_selected_stocks, print_config
from llm_processor import LLMProcessor
from output_formatter import OutputFormatter
from stock_data import get_multiple_stocks, get_stock_data


class StockAnalysisAgent:
    """Tool-driven version of the stock analysis workflow."""

    def __init__(self, stocks: list = None, max_cycles: int = 3, confidence_threshold: float = 0.78, memory_path: str = None):
        if stocks is None:
            stocks = get_selected_stocks()

        self.stocks = stocks
        self.max_cycles = max_cycles
        self.confidence_threshold = confidence_threshold
        self.results = {}
        self.processor = LLMProcessor()
        self.memory_path = memory_path or os.path.join("./output", "agent_memory.json")
        self.run_memory = self._load_persistent_memory()
        self.run_memory["started_at"] = datetime.now().isoformat()
        self.run_memory["current_run_stocks"] = self.stocks

    def _default_memory(self) -> dict:
        return {
            "version": 1,
            "started_at": None,
            "last_run_at": None,
            "run_count": 0,
            "ticker_memory": {},
            "lessons": [],
            "plan_log": [],
            "run_history": [],
            "current_run_stocks": [],
        }

    def _load_persistent_memory(self) -> dict:
        default_memory = self._default_memory()
        if not os.path.exists(self.memory_path):
            return default_memory

        try:
            with open(self.memory_path, "r", encoding="utf-8") as file_handle:
                loaded = json.load(file_handle)
            if not isinstance(loaded, dict):
                return default_memory

            merged = {**default_memory, **loaded}
            merged["ticker_memory"] = loaded.get("ticker_memory", {}) or {}
            merged["lessons"] = loaded.get("lessons", []) or []
            merged["plan_log"] = loaded.get("plan_log", []) or []
            merged["run_history"] = loaded.get("run_history", []) or []
            merged["run_count"] = int(loaded.get("run_count", 0) or 0)
            return merged
        except (OSError, json.JSONDecodeError):
            return default_memory

    def _persist_memory(self):
        os.makedirs(os.path.dirname(self.memory_path), exist_ok=True)
        payload = {
            **self.run_memory,
            "last_run_at": datetime.now().isoformat(),
            "run_count": int(self.run_memory.get("run_count", 0) or 0),
        }
        with open(self.memory_path, "w", encoding="utf-8") as file_handle:
            json.dump(payload, file_handle, indent=2, default=str)

    def run(self):
        """Execute the autonomous analysis loop."""
        print("=" * 60)
        print("TOOL-DRIVEN STOCK ANALYSIS AGENT STARTED")
        print("=" * 60)
        print(f"Target stocks: {', '.join(self.stocks)}")
        print(f"Max cycles per ticker: {self.max_cycles}")
        print(f"Confidence threshold: {self.confidence_threshold}")
        print()

        stock_snapshots = get_multiple_stocks(self.stocks)

        for ticker in self.stocks:
            print(f"\nAgent analyzing {ticker}...")
            print("-" * 40)

            state = self._create_state(ticker, stock_snapshots[ticker])
            state["memory"]["recent_lessons"] = self.run_memory["lessons"][-5:]

            while state["cycle"] < self.max_cycles and not state["completed"]:
                state["cycle"] += 1
                plan = self.processor.plan_next_actions(ticker, self._plan_context(state), self.run_memory)
                state["plan_history"].append(plan)
                self.run_memory["plan_log"].append({
                    "ticker": ticker,
                    "cycle": state["cycle"],
                    "plan": plan,
                    "timestamp": datetime.now().isoformat(),
                })

                print(f"  PLAN {state['cycle']}: {plan['objective']}")
                self._apply_memory_updates(state, plan.get("memory_updates", []))
                self._execute_plan(state, plan.get("steps", []))

                decision = state["decision"] or {}
                if plan.get("stop") or (
                    decision and decision.get("confidence", 0) >= self.confidence_threshold and not decision.get("need_more_data")
                ):
                    state["completed"] = True
                    state["stop_reason"] = "confident_enough"
                    break

                requery = plan.get("requery", {}) or {}
                if requery.get("needed"):
                    if state["cycle"] >= self.max_cycles:
                        state["stop_reason"] = "max_cycles_reached"
                        break
                    print(f"  RE-QUERY: {requery['reason']}")
                    self._execute_tool(state, requery)
                    self._invalidate_derived_state(state)
                    state["memory"]["open_questions"].append(requery["reason"])
                    state["requery_count"] += 1
                    continue

                state["memory"]["open_questions"].append("Planner requested another pass")

            if not state["completed"] and not state["stop_reason"]:
                state["stop_reason"] = "max_cycles_reached"

            # Final fallback: if we don't have a decision, attempt one using available evidence
            if not state.get("decision"):
                try:
                    if not state.get("articles_text"):
                        state["articles_text"] = format_articles_for_processing(state.get("articles", []))
                    if not state.get("summary"):
                        state["summary"] = self.processor.summarize_articles(state["articles_text"])
                    if not state.get("sentiment"):
                        state["sentiment"] = self.processor.analyze_sentiment(state["articles_text"])
                    if not state.get("insights"):
                        state["insights"] = self.processor.generate_insights(
                            state["stock_data"], state["articles_text"], state["sentiment"]
                        )

                    fallback_decision = self.processor.decide_action(
                        state["stock_data"], state["summary"], state["sentiment"], state["articles_text"]
                    )
                    state["decision"] = fallback_decision or {}
                    self._trace_tool(state, "decide_action", {}, fallback_decision, "Final fallback decision")
                except Exception as exc:  # pragma: no cover - defensive fallback
                    state["decision"] = {"recommendation": "undecided", "confidence": 0, "need_more_data": True}
                    self._trace_tool(state, "decide_action", {}, state["decision"], f"Fallback decision error: {exc}")

            self.run_memory["ticker_memory"][ticker] = self._compress_memory(state["memory"])
            self.run_memory["lessons"].append(self._derive_lesson(state))
            self.results[ticker] = state

        print("\n" + "=" * 60)
        print("AGENT ANALYSIS COMPLETED")
        print("=" * 60)

        self.run_memory["run_count"] = int(self.run_memory.get("run_count", 0) or 0) + 1
        self.run_memory["run_history"].append(
            {
                "run_at": datetime.now().isoformat(),
                "stocks": self.stocks,
                "lessons": self.run_memory["lessons"][-5:],
                "ticker_count": len(self.results),
            }
        )
        self._persist_memory()

        return self.results

    def _create_state(self, ticker: str, stock_data: dict) -> dict:
        return {
            "ticker": ticker,
            "stock_data": stock_data,
            "articles": [],
            "articles_text": "",
            "summary": "",
            "sentiment": {},
            "insights": [],
            "decision": {},
            "cycle": 0,
            "requery_count": 0,
            "completed": False,
            "stop_reason": "",
            "plan_history": [],
            "tool_trace": [],
            "memory": {
                "facts": [],
                "open_questions": [],
                "signals": [],
                "recent_lessons": [],
            },
            "generated_at": datetime.now().isoformat(),
        }

    def _plan_context(self, state: dict) -> dict:
        return {
            "ticker": state["ticker"],
            "stock_data": state["stock_data"],
            "article_count": len(state["articles"]),
            "summary": state["summary"],
            "sentiment": state["sentiment"],
            "insights": state["insights"],
            "decision": state["decision"],
            "memory": state["memory"],
            "recent_tool_trace": state["tool_trace"][-4:],
            "cycle": state["cycle"],
        }

    def _apply_memory_updates(self, state: dict, updates: list):
        for update in updates:
            state["memory"]["facts"].append(update)

    def _execute_plan(self, state: dict, steps: list):
        for step in steps:
            self._execute_tool(state, step)

    def _execute_tool(self, state: dict, step: dict):
        tool_name = step.get("tool")
        arguments = step.get("arguments", {}) or {}
        reason = step.get("reason", "")

        if tool_name == "fetch_stock_snapshot":
            output = get_stock_data(state["ticker"])
            state["stock_data"] = output
            self._trace_tool(state, tool_name, arguments, output, reason)
            return

        if tool_name == "fetch_articles":
            count = int(arguments.get("count", 3))
            output = get_stock_articles(state["ticker"], count=count)
            state["articles"] = self._merge_articles(state["articles"], output)
            state["articles_text"] = format_articles_for_processing(state["articles"])
            self._trace_tool(state, tool_name, {"count": count}, output, reason)
            return

        if tool_name == "format_articles":
            output = format_articles_for_processing(state["articles"])
            state["articles_text"] = output
            self._trace_tool(state, tool_name, arguments, output, reason)
            return

        if tool_name == "summarize_articles":
            if not state["articles_text"]:
                state["articles_text"] = format_articles_for_processing(state["articles"])
            output = self.processor.summarize_articles(state["articles_text"])
            state["summary"] = output
            self._trace_tool(state, tool_name, arguments, output, reason)
            return

        if tool_name == "analyze_sentiment":
            if not state["articles_text"]:
                state["articles_text"] = format_articles_for_processing(state["articles"])
            output = self.processor.analyze_sentiment(state["articles_text"])
            state["sentiment"] = output
            self._trace_tool(state, tool_name, arguments, output, reason)
            return

        if tool_name == "generate_insights":
            if not state["articles_text"]:
                state["articles_text"] = format_articles_for_processing(state["articles"])
            if not state["sentiment"]:
                state["sentiment"] = self.processor.analyze_sentiment(state["articles_text"])
            output = self.processor.generate_insights(state["stock_data"], state["articles_text"], state["sentiment"])
            state["insights"] = output
            self._trace_tool(state, tool_name, arguments, output, reason)
            return

        if tool_name == "decide_action":
            if not state["articles_text"]:
                state["articles_text"] = format_articles_for_processing(state["articles"])
            if not state["summary"]:
                state["summary"] = self.processor.summarize_articles(state["articles_text"])
            if not state["sentiment"]:
                state["sentiment"] = self.processor.analyze_sentiment(state["articles_text"])
            output = self.processor.decide_action(state["stock_data"], state["summary"], state["sentiment"], state["articles_text"])
            state["decision"] = output
            self._trace_tool(state, tool_name, arguments, output, reason)
            return

        raise ValueError(f"Unknown tool requested: {tool_name}")

    def _trace_tool(self, state: dict, tool_name: str, arguments: dict, output, reason: str):
        state["tool_trace"].append(
            {
                "tool": tool_name,
                "arguments": arguments,
                "reason": reason,
                "timestamp": datetime.now().isoformat(),
                "output": self._summarize_output(output),
            }
        )

        if tool_name in {"fetch_articles", "analyze_sentiment", "decide_action"}:
            state["memory"]["signals"].append(f"{tool_name}: {self._summarize_output(output)}")

    def _summarize_output(self, output):
        if isinstance(output, dict):
            compact = {}
            for key in ("overall_sentiment", "confidence", "recommendation", "need_more_data", "trend", "volatility"):
                if key in output:
                    compact[key] = output[key]
            return compact or output

        if isinstance(output, list):
            return output[:3]

        text = str(output).strip()
        return text[:240]

    def _invalidate_derived_state(self, state: dict):
        state["summary"] = ""
        state["sentiment"] = {}
        state["insights"] = []
        state["decision"] = {}
        state["memory"]["facts"].append("Derived analysis cleared after re-query")

    def _merge_articles(self, existing_articles: list, new_articles: list) -> list:
        seen = set()
        merged = []

        for article in existing_articles + new_articles:
            key = (article.get("title", ""), article.get("published_at", ""))
            if key in seen:
                continue
            seen.add(key)
            merged.append(article)

        return merged

    def _compress_memory(self, memory: dict) -> dict:
        return {
            "facts": memory.get("facts", [])[-8:],
            "open_questions": memory.get("open_questions", [])[-8:],
            "signals": memory.get("signals", [])[-8:],
            "recent_lessons": memory.get("recent_lessons", [])[-5:],
        }

    def _derive_lesson(self, state: dict) -> str:
        decision = state.get("decision", {}) or {}
        sentiment = state.get("sentiment", {}) or {}
        return (
            f"{state['ticker']}: {decision.get('recommendation', 'undecided').upper()} "
            f"with confidence {decision.get('confidence', 0)} after {state['cycle']} cycle(s); "
            f"sentiment={sentiment.get('overall_sentiment', 'unknown')}"
        )

    def _final_state_for_storage(self, state: dict) -> dict:
        return {
            "ticker": state["ticker"],
            "stock_data": state["stock_data"],
            "articles": state["articles"],
            "summary": state["summary"],
            "sentiment": state["sentiment"],
            "insights": state["insights"],
            "decision": state["decision"],
            "cycle": state["cycle"],
            "requery_count": state["requery_count"],
            "completed": state["completed"],
            "stop_reason": state["stop_reason"],
            "plan_history": state["plan_history"],
            "tool_trace": state["tool_trace"],
            "memory": state["memory"],
            "generated_at": state["generated_at"],
        }

    def generate_report(self) -> str:
        """Generate an agent-oriented report from results."""
        report = "AUTONOMOUS STOCK ANALYSIS REPORT\n"
        report += f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        report += "=" * 60 + "\n\n"

        for ticker, state in self.results.items():
            stock = state["stock_data"]
            decision = state["decision"] or {}
            sentiment = state["sentiment"] or {}

            report += f"TICKER: {ticker}\n"
            report += "-" * 40 + "\n"
            report += f"Current Price: ${stock['current_price']}\n"
            report += f"Trend: {stock['trend'].upper()}\n"
            report += f"Volatility: {stock['volatility']}\n"
            report += f"Cycles: {state['cycle']}\n"
            report += f"Re-queries: {state['requery_count']}\n"
            report += f"Decision: {decision.get('recommendation', 'undecided').upper()}\n"
            report += f"Confidence: {decision.get('confidence', 'n/a')}\n"
            report += f"Need More Data: {decision.get('need_more_data', False)}\n"
            report += f"Sentiment: {sentiment.get('overall_sentiment', 'unknown')}\n"
            report += f"Stop Reason: {state['stop_reason']}\n\n"

            report += "PLAN TRACE:\n"
            for index, plan in enumerate(state.get("plan_history", []), 1):
                requery = plan.get("requery", {})
                report += (
                    f"{index}. {plan.get('objective', 'Plan')} | "
                    f"steps={len(plan.get('steps', []))} | "
                    f"requery={requery.get('needed', False)}\n"
                )

            report += "\nTOOL TRACE:\n"
            for entry in state.get("tool_trace", [])[-10:]:
                report += f"- {entry['tool']}: {entry['reason']}\n"

            report += "\nMEMORY NOTES:\n"
            for fact in state.get("memory", {}).get("facts", [])[-5:]:
                report += f"- {fact}\n"

            if decision.get("evidence_gaps"):
                report += "\nEVIDENCE GAPS:\n"
                for gap in decision["evidence_gaps"]:
                    report += f"- {gap}\n"

            report += "\nKEY INSIGHTS:\n"
            for index, insight in enumerate(state.get("insights", []), 1):
                report += f"{index}. {insight}\n"

            report += "\n" + "=" * 60 + "\n\n"

        return report

    def save_outputs(self, output_dir: str = "./output"):
        """Save the agent outputs using the shared formatter."""
        os.makedirs(output_dir, exist_ok=True)

        formatter = OutputFormatter(self.results)
        saved_files = formatter.save_all_formats(output_dir)

        agent_report_path = os.path.join(output_dir, "agent_report.txt")
        with open(agent_report_path, "w", encoding="utf-8") as file_handle:
            file_handle.write(self.generate_report())
        saved_files.append(agent_report_path)

        agent_state_path = os.path.join(output_dir, "agent_state.json")
        with open(agent_state_path, "w", encoding="utf-8") as file_handle:
            json.dump(
                {
                    "generated_at": datetime.now().isoformat(),
                    "run_memory": self.run_memory,
                    "stocks": {ticker: self._final_state_for_storage(state) for ticker, state in self.results.items()},
                },
                file_handle,
                indent=2,
                default=str,
            )
        saved_files.append(agent_state_path)

        self._persist_memory()

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
