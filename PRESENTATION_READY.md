# Presentation Ready Notes

Event: Build //localhost:Mbarara
Date: June 13, 2026
Talk: Deploy, Observe, Learn. Reinforcement learning for production agents

## Fast Start

Run this from `C:\Users\ULTIMATE-INVESTOR\Downloads\AI Agents`:

```powershell
powershell -ExecutionPolicy Bypass -File .\START_DEMO.ps1
```

Open:

```text
http://127.0.0.1:8502
```

The launcher forces a stable demo mode:

- `USE_REAL_APIS=false`
- `USE_MOCK_LLM=true`
- `PYTHONIOENCODING=utf-8`

This avoids network delays, API quota surprises, and Windows console encoding crashes.

## 10 Minute Presenter Flow

1. Opening: "Today I am showing the difference between a fixed AI workflow and a production-style agent loop."
2. Point at the title: "Deploy, Observe, Learn is the lifecycle. Deploy the system, observe its evidence and decisions, then feed lessons back into future runs."
3. Run workflow mode first with 2 or 3 stocks.
4. Explain: "The workflow is predictable. It always executes the same path: data, articles, summary, sentiment, report."
5. Switch to agent mode and run the same stocks.
6. Explain: "The agent has a planner, tool calls, re-querying, decision confidence, and memory."
7. Open the Memory tab.
8. Explain: "This is the learning surface. In real production, this would connect to evaluation, feedback, monitoring, and policy updates."
9. Close with: "The important engineering question is not 'Can the model answer?' It is 'Can the system observe outcomes, improve behavior, and stay reliable in production?'"

## One Minute Backup Demo

If the browser is slow, use the terminal:

```powershell
cd .\workflow-project
$env:USE_REAL_APIS="false"
$env:USE_MOCK_LLM="true"
..\.venv\Scripts\python.exe main_workflow.py --agent --stocks AAPL MSFT TSLA
```

If that path is mistyped on stage, use the simpler command:

```powershell
python main_workflow.py --agent --stocks AAPL MSFT TSLA
```

## Key Lines To Say

- "A workflow is reliable because it is fixed."
- "An agent is flexible because it can decide what to do next."
- "Production readiness comes from observability: traces, confidence, memory, and fallback behavior."
- "Reinforcement learning in production is less about magic and more about closing the loop between actions, observations, rewards, and policy updates."

## Demo Safety Checklist

- Run the launcher before your session starts.
- Keep the browser open at `http://127.0.0.1:8502`.
- Run workflow first, then agent.
- Keep stock selection small: `AAPL`, `MSFT`, `TSLA`.
- Do not depend on live APIs unless you intentionally want internet variability.
