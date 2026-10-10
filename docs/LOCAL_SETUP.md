# Code-Archon: Local Setup (Windows)

This guide covers setting up Code-Archon on a new Windows machine after cloning the repository. It assumes PowerShell and uses the `feature/live-observability-ui` branch.

## 1. Prerequisites

Install:

- **Git** — to clone the repository.
- **Python 3.11 or newer** — required by `pyproject.toml`.
- **PowerShell** — included with Windows.

Optional:

- **Docker Desktop** — to run the included Neo4j and Redis services.
- **Graphviz** — install the system application (the `dot` executable) if you want Graphviz-generated images. The Python package alone may not provide the executable.
- **Groq API key** — needed for LLM-powered investigations with the default configuration.

## 2. Clone the repository

Open PowerShell:

```powershell
git clone -b feature/live-observability-ui https://github.com/Madhav-Ahuja27/Code-Archon.git
cd Code-Archon
```

If you want another branch, replace `feature/live-observability-ui` with its name.

## 3. Create and activate a virtual environment

From the repository root:

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
```

If PowerShell blocks virtual-environment activation, run this in the same terminal and try activating again:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

This policy change applies only to the current PowerShell process.

## 4. Install the project

Install Code-Archon and its development/test dependencies:

```powershell
python -m pip install -e ".[dev]"
```

Check that the commands are available:

```powershell
archon --help
archon-ui --help
```

If the commands are not found, confirm that the virtual environment is activated and rerun the install command.

## 5. Configure the LLM (recommended)

Copy the example configuration and open it:

```powershell
Copy-Item .env.example .env
notepad .env
```

Set your own API key and confirm the provider/model settings:

```dotenv
GROQ_API_KEY=your_actual_groq_api_key
LLM_PROVIDER=groq
LLM_MODEL=openai/gpt-oss-120b
```

Keep the other settings at their example defaults initially. Do not commit `.env` or share your API key. The configured model must be available to your API account; Code-Archon attempts to select a compatible Groq model if the requested one is unavailable.

If you do not have an API key, you can try a non-LLM run with `--no-llm`. Goal decomposition and investigation will be more limited.

## 6. Optional: start Neo4j and Redis

The repository includes `docker-compose.yml` for Neo4j and Redis. If Docker Desktop is installed and running, start them with:

```powershell
docker compose up -d
docker compose ps
```

The configured local endpoints are:

- Neo4j browser: http://localhost:7474
- Neo4j Bolt: `bolt://localhost:7687`
- Redis: `localhost:6379`

The Compose file configures Neo4j with username `neo4j` and password `archon-dev`. These are development defaults; change them before using this setup in any shared or exposed environment.

**Docker is optional for a first run.** The investigation code can fall back to an in-memory graph when Neo4j is unreachable, but the graph will not be persisted or browsable. Redis is included as a supporting service and is not required for the main investigation path described here.

## 7. Launch the web UI

With the virtual environment activated, run:

```powershell
archon-ui
```

By default, the server binds to `127.0.0.1:8765` and attempts to open a browser. Keep this terminal open while using the UI.

The server exposes these pages:

| Page | URL | Purpose |
|---|---|---|
| Customer UI | http://127.0.0.1:8765/ | Main starting page |
| Developer launcher | http://127.0.0.1:8765/dev | Configure and launch an investigation |
| Live observability | http://127.0.0.1:8765/live | View run events/logs and infrastructure information |

These pages are served by the same local process; you do not start three separate servers.

If port 8765 is already in use, choose another port:

```powershell
archon-ui --port 8766
```

Only bind the UI to a trusted interface. The UI can launch investigations on the host machine; do not expose it to an untrusted network.

## 8. Run your first investigation

In the developer launcher (`/dev`):

1. Enter the **absolute path** to the Python repository you want to analyze, for example `C:\Projects\some-python-project`.
2. Enter a goal, such as: `Explain the architecture, main execution flow, and important dependencies.`
3. Leave the iteration limit at its default for the first run.
4. Start the investigation and watch the logs/progress.

The repository being analyzed can be a different folder from the Code-Archon project itself.

## 9. Run from the CLI instead

You can run an investigation without the web UI:

```powershell
archon investigate "C:\Projects\some-python-project" `
  --goal "Explain the architecture and main execution flow" `
  --output ".\output"
```

For a non-LLM run:

```powershell
archon investigate "C:\Projects\some-python-project" `
  --goal "Summarize the modules and their relationships" `
  --no-llm
```

## 10. Find the generated results

After a successful run, open the generated `index.html` in a browser. With the default CLI output directory, the output is under `output\`.

Expected artifacts include:

- `index.html` — interactive investigation results dashboard.
- `report.md` — written investigation report.
- `modules\` — generated module documentation.
- `architecture.png` and `callgraph.png` — architecture and call-graph images, when generation succeeds.
- `session.db` — saved session/iteration data.

The **results dashboard** describes what the investigation discovered. The **live observability page** is for watching the run and checking diagnostic information; it is not the same dashboard.

## Troubleshooting

| Problem | What to check |
|---|---|
| `archon` or `archon-ui` is not recognized | Activate `.venv` and rerun `python -m pip install -e ".[dev]"`. |
| LLM/API error | Check `.env`, API key, provider, and whether the model is available to your account. |
| Neo4j is unreachable | Run `docker compose up -d`, or continue with the in-memory fallback if persistence is not needed. |
| Port 8765 is occupied | Run `archon-ui --port 8766`. |
| Graph images are missing | Check that Graphviz is installed and the `dot` executable is on `PATH`. |
| Findings are limited | Try a more specific goal, check `/live` logs, and verify LLM connectivity. |

## Quick-start checklist

- [ ] Python 3.11+ installed
- [ ] Repository cloned and virtual environment activated
- [ ] `python -m pip install -e ".[dev]"` completed
- [ ] `.env` configured if using an LLM
- [ ] Optional Docker services started if Neo4j persistence is desired
- [ ] `archon-ui` started, or a CLI investigation launched
- [ ] Generated `index.html` and `report.md` checked after the run
