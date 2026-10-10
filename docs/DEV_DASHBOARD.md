# Developer Dashboard

The developer dashboard is served at `http://127.0.0.1:8765/dev` by the same local server as the customer workspace and live observability page. It is intended for tuning, repeatable investigations, and diagnosing parser/index/graph issues.

## Advanced investigation controls

Open **Advanced developer controls** to configure:

- **LLM provider and model:** override `LLM_PROVIDER` and `LLM_MODEL` for this run only. API keys must already be configured in `.env`. Supported providers are Groq, OpenAI, and Anthropic.
- **Retrieval top-k:** source chunks retrieved for each task before retry widening.
- **Context token budget:** maximum approximate context size applied to returned retrieval chunks.
- **Tool calls per tool / iteration:** limits tool use within each agent iteration.
- **Evidence items per task:** caps evidence collected by retrieval, keyword search, and graph neighbours.
- **Evidence items in LLM prompt:** caps how many balanced evidence items are shown to the model.
- **Iteration limit:** limits the agent loop.
- **Keep existing Neo4j graph:** skips the default graph clear. Use only when intentionally retaining existing graph data; combining repositories can mix their nodes.
- **Session ID:** optionally choose a session identifier. Leave blank to generate one.
- **Explicit investigation tasks:** one task per line. Supplying tasks skips automatic goal decomposition.

Supported ranges are validated by the backend. These options are passed to the CLI, not just stored in the browser.

## Profiles

The profile selector includes four built-in presets:

- **Quick scan** — low-cost heuristic pass for a fast overview.
- **Architecture deep dive** — more iterations and a larger retrieval/evidence budget.
- **Routing and call flow** — tasks tailored to route registration, dispatch, middleware, handlers, and downstream calls.
- **Full documentation** — a larger LLM-assisted run intended for comprehensive documentation.

Use **Save profile** to store the current form configuration, **Load** to restore it, or **Delete** to remove a user-saved profile. User-saved profiles are stored in the current browser's local storage; they are not shared between browsers or machines. Built-in presets cannot be deleted.

## Graph and index inspector

After a run, expand **Graph & index inspector** in the investigation monitor. It reads `archon-diagnostics.json` from that run's output folder and lets you search:

- parsed modules, line counts, imports, dependencies, and average complexity;
- functions, arguments, calls, class membership, source ranges, and complexity;
- classes, bases, methods, and source ranges;
- parse errors;
- graph relationships, with source and target node IDs.

The summary metrics above the inspector report parser, graph, index, and agent counters extracted from actual CLI output. Detailed symbol data is emitted by the CLI after parsing/indexing. The inspector is unavailable if the run fails before that artifact is written.

## Execution controls

- **Cancel investigation** terminates the active CLI process.
- **Rerun with same configuration** copies the previous settings back into the form. A fresh session ID is used on submission to avoid accidental reuse.

The UI is designed for trusted local use. Keep the server bound to localhost and do not expose it to an untrusted network.
