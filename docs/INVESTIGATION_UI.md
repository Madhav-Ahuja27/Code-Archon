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

The **developer monitor** remains available at **http://127.0.0.1:8765/dev** for inspecting raw CLI output. The **live observability workspace** is at **http://127.0.0.1:8765/live** and is also linked from the customer page. The customer page is also available at `/app`.

Alternatively, run `python -m archon.webui`. Use `python -m archon.webui --no-browser` to suppress automatic browser launch, or `--port 8766` to select another local port.

## Use the customer workspace

1. Enter the local folder path to a repository checked out on the machine running Archon.
2. Ask a question in natural language or choose one of the suggested investigation prompts.
3. Choose an output folder outside the source repository and a depth setting.
4. Start the investigation. The workspace presents understandable progress while the existing CLI runs.
5. When complete, select **Explore investigation results** to open the generated dashboard.

The workspace currently runs LLM-assisted investigations using the configured Groq key. The developer monitor exposes the lower-level controls. Only one investigation can run at a time because the current graph-store setup clears and rebuilds graph state per run.

This is a local-first prototype: investigation history is held in memory by the UI server and will reset when the server restarts. Repository selection currently uses a local path rather than Git-provider OAuth or remote clone flow. Keep the server bound to `127.0.0.1`; it can launch processes against folders accessible to your account and should not be exposed to an untrusted network.

The generated investigation dashboard now has a dedicated **Not verified** panel. Tasks without a verified finding remain visible with an explicit **NOT VERIFIED** tag; unresolved and rejected items retain their more specific status and also carry **NOT VERIFIED**. Missing verification means unknown, not false.

During a live investigation, the customer progress modal shows the actual recorded event stream and host-service probes for Docker, Neo4j, and Redis. These probes are point-in-time diagnostics: service reachability alone does not prove that the active run uses that service. The event filters show only events emitted by the engine; a missing event is not evidence that a step did not happen.

The staged improvement plan and outstanding verification work are tracked in `docs/UI_IMPROVEMENT_ROADMAP.md`.

The UI does not change AST parsing, retrieval, graph building, agent behavior, evidence verification, or finding promotion.


## Live observability workspace

The `/live` workspace polls the actual run state and shows:

- Structured LangGraph node start/completion/failure events, phase, current task, iteration, evidence/finding counts, verification status, retries, and recorded tool-call inputs/output summaries/errors.
- The real CLI stdout/stderr captured by the launcher.
- A point-in-time Docker CLI snapshot for relevant containers, a Neo4j Bolt/authentication probe and graph node count when the driver is available, and Redis PING/basic metrics when reachable.

Structured traces are written as JSONL to `.archon-observability/<run-id>.jsonl` under the chosen output folder. They are best-effort and observational: trace write failures are swallowed so they do not change investigation behavior. Runs started before this instrumentation may only have process logs. Infrastructure data is a snapshot, not proof that the active investigation uses every reachable service; Code-Archon can fall back to in-memory graph or Redis stores.

The observability view can include source excerpts and tool inputs/outputs. Keep the UI bound to localhost and treat the output folder as sensitive. Hidden model chain-of-thought is not exposed; the UI shows operational events, evidence metadata, and returned outputs instead.
