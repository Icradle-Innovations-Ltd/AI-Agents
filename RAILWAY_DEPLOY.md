# Deploying To Railway

This repository is ready to deploy as a Streamlit service on Railway.

## Railway Settings

Use the default repository root. The root `requirements.txt` installs the Python dependencies from `workflow-project/requirements.txt`, and `railway.toml` starts Streamlit from the app directory.

Start command:

```bash
cd workflow-project && streamlit run app.py --server.address 0.0.0.0 --server.port $PORT --server.headless true
```

## Recommended Variables

For a stable public demo:

```text
USE_REAL_APIS=false
USE_MOCK_LLM=true
PYTHONIOENCODING=utf-8
```

For real API mode, set these in Railway service variables:

```text
USE_REAL_APIS=true
USE_MOCK_LLM=false
OPENAI_API_KEY=...
ALPHAVANTAGE_API_KEY=...
NEWSAPI_KEY=...
```

Do not commit `.env` files or API keys.
