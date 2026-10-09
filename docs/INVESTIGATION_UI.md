# Code-Archon browser interfaces

Code-Archon provides a customer-facing workspace and a separate developer monitor. Both run locally and launch the existing `archon.cli investigate` command; neither reimplements the investigation pipeline.

## Start

After the normal project setup:

```powershell
pip install -e ".[dev]"
Copy-Item .env.example .env
# Add your GROQ_API_KEY to .env
docker-compose up -d
python -m pytest tests/ -q
archon-ui
```

The customer workspace opens at **http://127.0.0.1:8765**. It provides a natural-language investigation form, suggested questions, recent investigation history for the current server session, progress in plain language, and a link to the generated interactive dashboard.

The **developer monitor** remains available at **http://127.0.0.1:8765/dev** for inspecting raw CLI output. The customer page is also available at `/app`.

Alternatively, run `python -m archon.webui`. Use `python -m archon.webui --no-browser` to suppress automatic browser launch, or `--port 8766` to select another local port.

## Use the customer workspace

1. Enter the local folder path to a repository checked out on the machine running Archon.
2. Ask a question in natural language or choose one of the suggested investigation prompts.
3. Choose an output folder outside the source repository and a depth setting.
4. Start the investigation. The workspace presents understandable progress while the existing CLI runs.
5. When complete, select **Explore investigation results** to open the generated dashboard.

The workspace currently runs LLM-assisted investigations using the configured Groq key. The developer monitor exposes the lower-level controls. Only one investigation can run at a time because the current graph-store setup clears and rebuilds graph state per run.

This is a local-first prototype: investigation history is held in memory by the UI server and will reset when the server restarts. Repository selection currently uses a local path rather than Git-provider OAuth or remote clone flow. Keep the server bound to `127.0.0.1`; it can launch processes against folders accessible to your account and should not be exposed to an untrusted network.

The UI does not change AST parsing, retrieval, graph building, agent behavior, evidence verification, or finding promotion.
