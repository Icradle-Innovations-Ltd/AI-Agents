param(
    [int]$Port = 8502
)

$ErrorActionPreference = "Stop"

$RepoRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$ProjectRoot = Join-Path $RepoRoot "workflow-project"
$VenvPython = Join-Path $RepoRoot ".venv\Scripts\python.exe"
$Python = if (Test-Path $VenvPython) { $VenvPython } else { "python" }

# Keep the presentation path stable and fast. The real API keys in .env remain untouched.
$env:PYTHONIOENCODING = "utf-8"
$env:USE_REAL_APIS = "false"
$env:USE_MOCK_LLM = "true"

Set-Location $ProjectRoot
Write-Host "Starting Deploy, Observe, Learn demo on http://127.0.0.1:$Port"
& $Python -m streamlit run app.py --server.port $Port --server.headless true
