"""
Streamlit dashboard for the stock analysis workflow and tool-driven agent.
"""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

import streamlit as st

from agent_tool_driven import StockAnalysisAgent
from config import OUTPUT_FORMATS, STOCKS, get_selected_stocks
from main_workflow import StockAnalysisWorkflow


APP_TITLE = "Deploy, Observe, Learn"
APP_SUBTITLE = "Production agents need a loop: run, inspect, re-query, remember."
OUTPUT_DIR = Path("output")
MEMORY_PATH = OUTPUT_DIR / "agent_memory.json"
DEFAULT_DEMO_STOCKS = ["AAPL", "MSFT", "TSLA"]


st.set_page_config(
    page_title=f"{APP_TITLE} | Stock Intelligence Studio",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="collapsed",
)


def inject_styles():
    st.markdown(
        """
        <style>
        .stApp {
            background: #f7f8fb !important;
            color: #071133;
        }
        html, body, section[data-testid="stAppViewContainer"] {
            background: #f7f8fb !important;
            color: #071133 !important;
        }
        header[data-testid="stHeader"],
        div[data-testid="stToolbar"],
        div[data-testid="stDecoration"],
        #MainMenu,
        footer {
            display: none !important;
            visibility: hidden !important;
            height: 0 !important;
        }
        section[data-testid="stSidebar"],
        button[kind="header"],
        button[title="View fullscreen"] {
            display: none !important;
            visibility: hidden !important;
        }
        div[data-testid="stAppViewBlockContainer"] {
            max-width: 1180px !important;
            padding-top: 2.6rem !important;
            padding-left: 2rem !important;
            padding-right: 2rem !important;
        }
        .hero {
            padding: 1.7rem 2rem 1.35rem 2rem;
            border-radius: 8px;
            border: 1px solid rgba(19, 34, 56, 0.06);
            background: #ffffff;
            backdrop-filter: blur(6px);
            box-shadow: 0 10px 24px rgba(17, 24, 39, 0.06);
            margin-bottom: 1rem;
        }
        .eyebrow {
            text-transform: uppercase;
            letter-spacing: 0.12em;
            font-size: 0.72rem;
            font-weight: 700;
            color: #c46b1f;
            margin-bottom: 0.35rem;
        }
        .hero h1 {
            font-size: 2.55rem;
            line-height: 1.02;
            margin-bottom: 0.4rem;
            color: #0f1724;
        }
        .hero p {
            font-size: 1.03rem;
            max-width: 72ch;
            color: #334155;
            margin-bottom: 0;
        }
        .glass-card {
            padding: 1rem 1rem;
            border-radius: 8px;
            background: #ffffff;
            border: 1px solid rgba(19, 34, 56, 0.06);
            box-shadow: 0 8px 20px rgba(17, 24, 39, 0.05);
        }
        .metric-label {
            font-size: 0.72rem;
            text-transform: uppercase;
            letter-spacing: 0.12em;
            color: #475569;
            margin-bottom: 0.25rem;
        }
        .metric-value {
            font-size: 1.45rem;
            font-weight: 800;
            color: #071133;
            line-height: 1.15;
        }
        .metric-note {
            font-size: 0.9rem;
            color: #334155;
            margin-top: 0.3rem;
        }
        .section-title {
            font-size: 1.05rem;
            font-weight: 800;
            color: #071133;
            margin: 0.8rem 0 0.5rem 0;
        }
        .small-caps {
            text-transform: uppercase;
            letter-spacing: 0.12em;
            font-size: 0.72rem;
            color: #475569;
            font-weight: 700;
        }
        .summary-box {
            padding: 0.9rem 0.95rem;
            border-radius: 8px;
            background: #ffffff;
            border: 1px solid rgba(19, 34, 56, 0.06);
        }
        .status-pill {
            display: inline-block;
            padding: 0.32rem 0.7rem;
            border-radius: 999px;
            font-size: 0.74rem;
            font-weight: 700;
            background: #e6f0ff;
            color: #05386b;
            margin-right: 0.4rem;
        }
        .status-pill.agent {
            background: #fff4e6;
            color: #8a4b12;
        }
        .status-pill.workflow {
            background: #eaf8f1;
            color: #0f6b3f;
        }
        /* Improve button contrast and sizing */
        .stButton>button, .stButton button, button.stButton {
            background-color: #ffffff !important;
            color: #071133 !important;
            border: 1px solid rgba(7,17,51,0.06) !important;
            box-shadow: 0 6px 18px rgba(7, 17, 51, 0.06) !important;
            padding: 0.6rem 1rem !important;
            border-radius: 8px !important;
            font-weight: 700 !important;
        }
        .stButton>button:hover, .stButton button:hover {
            background-color: #f3f6fa !important;
        }
        /* Ensure wide container buttons align text correctly */
        .stButton>div, .stButton>button {
            text-align: center !important;
        }
        /* Improve captions, info boxes, and markdown contrast */
        .stCaption, .stMarkdown p, .stText, .stWrite {
            color: #071133 !important;
        }
        /* Streamlit info/alert boxes */
        .stAlert, .stInfo, div[data-testid="stInfo"] {
            background: rgba(230, 240, 255, 0.96) !important;
            border: 1px solid rgba(7, 17, 51, 0.06) !important;
            color: #071133 !important;
        }
        .stAlert p, .stInfo p, div[data-testid="stInfo"] p {
            color: #071133 !important;
        }
        /* Improve tab header contrast and selected state */
        div[role="tablist"] > button {
            color: #071133 !important;
            background: rgba(255,255,255,0.92) !important;
            border: 1px solid rgba(7,17,51,0.06) !important;
            font-weight: 800 !important;
            padding: 0.45rem 0.8rem !important;
            margin-right: 0.35rem !important;
            border-radius: 8px !important;
        }
        div[role="tablist"] > button[aria-selected="true"] {
            background: #e25332 !important;
            color: #ffffff !important;
            box-shadow: 0 8px 20px rgba(226,83,50,0.16) !important;
        }
        .control-band {
            background: #ffffff;
            border: 1px solid rgba(7,17,51,0.06);
            border-radius: 8px;
            box-shadow: 0 8px 20px rgba(17,24,39,0.05);
            padding: 0.9rem 1rem 0.4rem 1rem;
            margin: 0.2rem 0 1rem 0;
        }
        .control-band-title {
            font-size: 0.72rem;
            font-weight: 800;
            letter-spacing: 0.12em;
            text-transform: uppercase;
            color: #475569;
            margin-bottom: 0.5rem;
        }
        div[data-baseweb="select"] > div {
            background: #ffffff !important;
            border: 1px solid rgba(7,17,51,0.12) !important;
            box-shadow: 0 4px 14px rgba(17,24,39,0.04) !important;
        }
        div[data-baseweb="select"] svg {
            color: #071133 !important;
            fill: #071133 !important;
        }
        div[data-baseweb="tag"] {
            background: #f0524d !important;
            color: #ffffff !important;
            border-radius: 6px !important;
        }
        div[data-baseweb="tag"] span,
        div[data-baseweb="tag"] svg {
            color: #ffffff !important;
            fill: #ffffff !important;
        }
        div[role="tablist"] > button[aria-selected="true"] * {
            color: #ffffff !important;
        }

        /* Ensure the main app container can scroll vertically on overflow */
        html, body, .stApp, section[data-testid="stAppViewContainer"] {
            height: 100% !important;
        }
        div[data-testid="stAppViewBlockContainer"] {
            max-height: 100vh !important;
            overflow-y: auto !important;
        }

        /* Custom scrollbar for WebKit browsers */
        section[data-testid="stAppViewContainer"] > div::-webkit-scrollbar {
            width: 12px;
        }
        section[data-testid="stAppViewContainer"] > div::-webkit-scrollbar-track {
            background: rgba(15,23,36,0.03);
            border-radius: 8px;
        }
        section[data-testid="stAppViewContainer"] > div::-webkit-scrollbar-thumb {
            background: rgba(7,17,51,0.12);
            border-radius: 8px;
        }
        /* Ensure all textual elements are readable against backgrounds */
        .stApp *:not(svg) {
            color: #071133 !important;
        }

        /* Keep the projector/demo theme stable even when the OS uses dark mode. */
        @media (prefers-color-scheme: dark) {
            html, body, .stApp, section[data-testid="stAppViewContainer"] {
                background: #f7f8fb !important;
                color: #071133 !important;
            }
            .hero, .glass-card, .summary-box, .control-band, div[role="tabpanel"] {
                background: #ffffff !important;
                color: #071133 !important;
                border: 1px solid rgba(7,17,51,0.06) !important;
                box-shadow: 0 8px 20px rgba(17,24,39,0.05) !important;
            }
            .stButton>button, .stButton button, button.stButton {
                background-color: #ffffff !important;
                color: #071133 !important;
                border: 1px solid rgba(7,17,51,0.08) !important;
            }
        }

        /* Stronger rules for markdown content and headings */
        .stMarkdown h1, .stMarkdown h2, .stMarkdown h3, .stMarkdown h4, .stMarkdown p, .stMarkdown li {
            color: #071133 !important;
        }

        /* Ensure cards and summaries sit above decorative backgrounds */
        .hero, .glass-card, .summary-box, .control-band, .stTabs, div[role="tabpanel"] {
            background: #ffffff !important;
            z-index: 50 !important;
        }

        /* Make the pale info stripe more prominent */
        div[data-testid="stInfo"] {
            background: rgba(230,240,255,0.98) !important;
            color: #071133 !important;
            border: 1px solid rgba(7,17,51,0.06) !important;
        }
        @media (max-width: 900px) {
            div[data-testid="stAppViewBlockContainer"] {
                padding-left: 1rem !important;
                padding-right: 1rem !important;
            }
            .hero h1 {
                font-size: 2rem;
            }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def load_agent_memory() -> dict:
    if not MEMORY_PATH.exists():
        return {}
    try:
        return json.loads(MEMORY_PATH.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}


def pick_stocks() -> list[str]:
    default_stocks = [ticker for ticker in DEFAULT_DEMO_STOCKS if ticker in STOCKS]
    selected = st.multiselect(
        "Stocks to analyze",
        options=list(STOCKS.keys()),
        default=default_stocks or get_selected_stocks()[:3],
    )
    return selected or get_selected_stocks()[:3]


def render_hero():
    st.markdown(
        f"""
        <div class="hero">
            <div class="eyebrow">Build //localhost:Mbarara</div>
            <h1>{APP_TITLE}</h1>
            <p>{APP_SUBTITLE}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_overview(mode: str, stocks: list[str], memory: dict):
    cols = st.columns(4)
    with cols[0]:
        st.markdown(
            f"""
            <div class="glass-card">
                <div class="metric-label">Mode</div>
                <div class="metric-value">{mode.title()}</div>
                <div class="metric-note">{('Fixed sequence' if mode == 'workflow' else 'Planner-driven with memory')}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with cols[1]:
        st.markdown(
            f"""
            <div class="glass-card">
                <div class="metric-label">Stocks</div>
                <div class="metric-value">{len(stocks)}</div>
                <div class="metric-note">{', '.join(stocks)}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with cols[2]:
        runs = memory.get("run_count", 0) if isinstance(memory, dict) else 0
        st.markdown(
            f"""
            <div class="glass-card">
                <div class="metric-label">Learn Loop</div>
                <div class="metric-value">{runs}</div>
                <div class="metric-note">Persisted lessons from agent runs</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with cols[3]:
        st.markdown(
            f"""
            <div class="glass-card">
                <div class="metric-label">Demo Signal</div>
                <div class="metric-value">TSLA</div>
                <div class="metric-note">Volatility should trigger watch/re-query</div>
            </div>
            """,
            unsafe_allow_html=True,
        )


def render_demo_controls():
    st.markdown('<div class="control-band-title">Demo controls</div>', unsafe_allow_html=True)
    control_cols = st.columns([1.2, 2.2, 0.9, 0.9])
    with control_cols[0]:
        mode = st.radio("Mode", ["workflow", "agent"], index=1, horizontal=True)
    with control_cols[1]:
        stocks = pick_stocks()
    with control_cols[2]:
        show_memory = st.checkbox("Memory", value=True)
    with control_cols[3]:
        run_outputs = st.checkbox("Save", value=True)

    return mode, stocks, show_memory, run_outputs


def render_results_table(results: dict):
    rows = []
    for ticker, data in results.items():
        stock = data.get("stock_data", {})
        decision = data.get("decision", {})
        sentiment = data.get("sentiment", {})
        rows.append(
            {
                "Ticker": ticker,
                "Price": stock.get("current_price"),
                "Change %": stock.get("change_percent"),
                "Trend": stock.get("trend"),
                "Sentiment": sentiment.get("overall_sentiment", decision.get("overall_sentiment", "n/a")),
                "Confidence": sentiment.get("confidence", decision.get("confidence", "n/a")),
                "Decision": decision.get("recommendation", "n/a"),
            }
        )
    st.dataframe(rows, use_container_width=True, hide_index=True)


def render_workflow_results(results: dict):
    for ticker, data in results.items():
        stock = data.get("stock_data", {})
        sentiment = data.get("sentiment", {})
        columns = st.columns([1.3, 1.1, 1.2])
        with columns[0]:
            st.markdown(
                f"""
                <div class="summary-box">
                    <div class="small-caps">{ticker}</div>
                    <h3 style="margin:0.2rem 0 0.5rem 0;">Workflow Output</h3>
                    <div class="status-pill workflow">Fixed workflow</div>
                    <div class="metric-note" style="margin-top:0.75rem;">{data.get('summary', '')}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
        with columns[1]:
            st.metric("Current Price", f"${stock.get('current_price', 'n/a')}")
            st.metric("Trend", stock.get("trend", "n/a").upper())
            st.metric("Volatility", stock.get("volatility", "n/a"))
        with columns[2]:
            st.metric("Sentiment", sentiment.get("overall_sentiment", "n/a").upper())
            st.metric("Confidence", sentiment.get("confidence", "n/a"))
            st.write("Insights")
            for insight in data.get("insights", []):
                st.write(f"- {insight}")
        st.divider()


def render_agent_results(results: dict):
    for ticker, state in results.items():
        stock = state.get("stock_data", {})
        decision = state.get("decision", {})
        sentiment = state.get("sentiment", {})
        cols = st.columns([1.2, 1.0, 1.3])
        with cols[0]:
            st.markdown(
                f"""
                <div class="summary-box">
                    <div class="small-caps">{ticker}</div>
                    <h3 style="margin:0.2rem 0 0.5rem 0;">Agent Output</h3>
                    <div>
                        <span class="status-pill agent">Autonomous agent</span>
                        <span class="status-pill">{state.get('cycle', 0)} cycles</span>
                    </div>
                    <div class="metric-note" style="margin-top:0.75rem;">Decision: {decision.get('recommendation', 'n/a').upper()} | Stop reason: {state.get('stop_reason', 'n/a')}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
        with cols[1]:
            st.metric("Current Price", f"${stock.get('current_price', 'n/a')}")
            st.metric("Re-queries", state.get("requery_count", 0))
            st.metric("Confidence", decision.get("confidence", "n/a"))
        with cols[2]:
            st.write("Plan Trace")
            for plan in state.get("plan_history", []):
                st.write(f"- {plan.get('objective', 'Plan')}")
            st.write("Memory Notes")
            for fact in state.get("memory", {}).get("facts", [])[-4:]:
                st.write(f"- {fact}")
            st.write("Latest Sentiment")
            st.write(f"{sentiment.get('overall_sentiment', 'n/a')} ({sentiment.get('confidence', 'n/a')})")
        st.divider()


def render_memory_panel(memory: dict):
    st.markdown('<div class="section-title">Persistent Agent Memory</div>', unsafe_allow_html=True)
    if not memory:
        st.info("No persisted memory yet. Run the agent once and it will create output/agent_memory.json.")
        return

    cols = st.columns(3)
    with cols[0]:
        st.metric("Run Count", memory.get("run_count", 0))
    with cols[1]:
        st.metric("Lessons Stored", len(memory.get("lessons", [])))
    with cols[2]:
        st.metric("Plan Entries", len(memory.get("plan_log", [])))

    st.write("Recent lessons")
    for lesson in memory.get("lessons", [])[-6:]:
        st.write(f"- {lesson}")

    st.write("Latest run history")
    for run in memory.get("run_history", [])[-5:]:
        st.write(f"- {run.get('run_at', 'n/a')} | stocks: {', '.join(run.get('stocks', []))} | tickers: {run.get('ticker_count', 0)}")


def main():
    inject_styles()
    render_hero()

    mode, stocks, show_memory, run_outputs = render_demo_controls()

    memory = load_agent_memory() if show_memory else {}
    render_overview(mode, stocks, memory)

    st.markdown('<div class="section-title">Run the engine</div>', unsafe_allow_html=True)
    left, right = st.columns([1, 1])
    with left:
        workflow_button = st.button("Run workflow", use_container_width=True)
    with right:
        agent_button = st.button("Run agent", use_container_width=True)

    results = st.session_state.get("results", {})
    active_mode = st.session_state.get("active_mode", mode)

    if workflow_button or (mode == "workflow" and not agent_button and st.session_state.get("auto_run", False)):
        active_mode = "workflow"
        with st.spinner("Running fixed workflow..."):
            workflow = StockAnalysisWorkflow(stocks=stocks)
            results = workflow.run()
            if run_outputs:
                workflow.save_outputs(str(OUTPUT_DIR))
            st.session_state["results"] = results
            st.session_state["active_mode"] = active_mode
            st.session_state["auto_run"] = False

    if agent_button or (mode == "agent" and not workflow_button and st.session_state.get("auto_run", False)):
        active_mode = "agent"
        with st.spinner("Running tool-driven agent..."):
            agent = StockAnalysisAgent(stocks=stocks)
            results = agent.run()
            if run_outputs:
                agent.save_outputs(str(OUTPUT_DIR))
            st.session_state["results"] = results
            st.session_state["active_mode"] = active_mode
            st.session_state["auto_run"] = False
            memory = load_agent_memory()

    if results:
        tab_results, tab_details, tab_memory = st.tabs(["Results", "Details", "Memory"])
        with tab_results:
            render_results_table(results)
        with tab_details:
            if active_mode == "workflow":
                render_workflow_results(results)
            else:
                render_agent_results(results)
        with tab_memory:
            render_memory_panel(load_agent_memory())
    else:
        st.info("Ready for the live demo.")


if __name__ == "__main__":
    main()
