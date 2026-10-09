# Code-Archon — End-to-End Usage Guide

**AI Archaeologist — Autonomous Legacy Software Reverse-Engineering**

---

## Prerequisites

| Requirement | Version | Notes |
|-------------|---------|-------|
| Python | 3.11+ | `python3 --version` |
| pip | latest | `pip install --upgrade pip` |
| Docker + Compose | any | Optional — needed for Neo4j + Redis |
| Git | any | For `git_log`, `git_blame` tools |
| ripgrep (`rg`) | any | Optional — falls back to `grep` |
| Graphviz (`dot`) | any | Optional — falls back to placeholder PNG |

---

## 1. Installation

### 1.1 Clone and install

```bash
# Unpack the tarball
tar xzf code-archon-final.tar.gz
cd code-archon

# Install in editable mode with dev extras
pip install -e ".[dev]"
```

### 1.2 Configure environment

```bash
cp .env.example .env
```

Edit `.env`:

```env
# Required: LLM provider (Groq is free)
GROQ_API_KEY=gsk_your_key_here
LLM_PROVIDER=groq
LLM_MODEL=llama-3.3-70b-versatile

# Optional: alternative LLMs
# ANTHROPIC_API_KEY=sk-ant-...
# LLM_PROVIDER=anthropic
# LLM_MODEL=claude-sonnet-4-6

# Infrastructure (optional — in-memory fallbacks used if unavailable)
NEO4J_URI=bolt://localhost:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=archon-dev
REDIS_URL=redis://localhost:6379

# Storage
CHROMA_PATH=./data/chroma

# Agent tuning
MAX_AGENT_ITERATIONS=20
MAX_CONTEXT_TOKENS=6000
TOOL_CALL_LIMIT_PER_ITER=5
```

### 1.3 Start infrastructure (optional but recommended)

```bash
docker-compose up -d
```

This starts Neo4j (port 7687 / 7474) and Redis (port 6379).

Without Docker, all data is stored in-memory and lost when the process ends. Sessions are still persisted in SQLite even without Redis/Neo4j.

---

## 2. Verify the installation

```bash
# Run the full test suite
python -m pytest tests/ -q

# Expected output:
# 141 passed, 4 skipped
# (4 skipped = Neo4j + Redis Docker tests + Groq egress tests in CI)
```

---

## 3. Core Command: `investigate`

```bash
python -m archon.cli investigate \
  --repo ./path/to/legacy-repo \
  --goal "Understand the authentication module and trace the login flow" \
  --output ./output/ \
  --max-iter 15
```

### Options

| Flag | Default | Description |
|------|---------|-------------|
| `--repo` | required | Path to the Python repository to investigate |
| `--goal`, `-g` | `"Understand the codebase architecture"` | Free-text investigation objective |
| `--output`, `-o` | `./output` | Directory to write documentation |
| `--max-iter`, `-n` | `10` | Maximum agent iterations |
| `--session-id` | auto-generated | Resume or label a session |
| `--llm` / `--no-llm` | `--llm` | Use Groq LLM or keyword-only mode |

### What it does — step by step

```
1. Parses every .py file in the repo
   → ModuleNode, ClassNode, FunctionNode per file

2. Populates the graph store
   → Neo4j (or in-memory) with confidence + provenance on every node

3. Builds retrieval index
   → BM25 keyword index + ChromaDB vector index

4. Decomposes your goal into investigation tasks
   → Groq LLM (or keyword fallback)

5. Runs the agent loop
   PLAN → ACT → OBSERVE → VERIFY → UPDATE_GRAPH
   → Verified claims written to graph with file:line provenance
   → Unverified claims trigger replanning
   → Hard stop at max-iter

6. Saves session to SQLite
   → output/session.db

7. Generates documentation
   → output/report.md
   → output/modules/
   → output/architecture.png
   → output/callgraph.png
```

### Example output

```
╭────────── Investigation Start ───────────────╮
│ Code-Archon — AI Archaeologist               │
│ Repo:    ./flask-v1.1.4                      │
│ Goal:    Understand the routing system       │
│ Session: sess_a3f72b1c                       │
╰──────────────────────────────────────────────╯

✓ Parsed: 23 modules, 187 functions, 0 errors
✓ Graph: 218 nodes
✓ Index: 210 chunks
✓ Goal decomposed into 3 tasks
  • map routing system
  • trace URL dispatch
  • identify view functions
✓ LLM connected

Running agent loop...

✓ Complete after 8 iterations
  Findings: 6

Documentation written → ./output/

  • ./output/report.md
  • ./output/modules/  (23 files)
  • ./output/architecture.png
  • ./output/callgraph.png
```

---

## 4. Without LLM (offline / keyword-only mode)

```bash
python -m archon.cli investigate \
  --repo ./path/to/legacy-repo \
  --goal "understand api dependencies" \
  --no-llm \
  --output ./output/
```

In `--no-llm` mode:
- Goal decomposition uses keyword pattern matching
- Agent verification uses heuristic (evidence present → VERIFIED)
- No API key required
- Fully offline

---

## 5. Regenerate documentation only

If you have already run an investigation and want to regenerate docs from the existing graph:

```bash
python -m archon.cli generate-docs sess_a3f72b1c --output ./output/
```

---

## 6. Python API (programmatic use)

### 6.1 Parse a repository

```python
from archon.ingestion.ast_parser import parse_repository
from pathlib import Path

result = parse_repository(Path("./my-legacy-repo"))

print(f"Modules: {len(result.modules)}")
print(f"Functions: {len(result.functions)}")
print(f"Classes: {len(result.classes)}")
print(f"Parse errors: {len(result.errors)}")

for mod in result.modules:
    print(f"  {mod.id}: {mod.line_count} lines, avg CC {mod.avg_complexity:.1f}")
```

### 6.2 Build and query the graph

```python
from archon.graph.neo4j_client import make_graph_store, GraphNode, GraphEdge
from archon.graph.network_graph import ArchonGraph

# Get a store (Neo4j if available, in-memory otherwise)
store = make_graph_store()

# Add a node
store.upsert_node(GraphNode(
    id="auth.py::hash_password",
    label="Function",
    properties={"name": "hash_password", "complexity": 3},
    confidence=0.9,
    provenance="auth.py:14",
))

# Query
node = store.get_node("auth.py::hash_password")
low_conf = store.low_confidence_nodes(threshold=0.5)

# NetworkX analysis
g = ArchonGraph()
g.sync_from_store(store)
print("Entry points:", g.find_entry_points())
print("Has cycle:", g.has_cycle())
print("Call chain:", g.get_call_chain("auth.py::login"))
```

### 6.3 Retrieve relevant context

```python
from archon.retrieval.bm25 import BM25Index
from archon.retrieval.vector_store import VectorStore, ContextEngine

# Build index from parse result
chunks = ContextEngine.chunks_from_parse_result(parse_result)

bm25 = BM25Index()
bm25.build(chunks)

vs = VectorStore(use_hash_embed=False)  # use MiniLM in production
vs.add_chunks(chunks)

engine = ContextEngine(bm25, vs, max_tokens=6000)

# Query
results = engine.query("authentication login password", top_k=10)
context_string = engine.build_context_window(results)
print(context_string[:500])
```

### 6.4 Run the agent loop directly

```python
from archon.agent.loop import AgentState, build_agent_graph
from archon.agent.harness import Harness, HarnessConfig
from archon.graph.neo4j_client import make_graph_store
from archon.llm import make_llm

store = make_graph_store()
llm = make_llm()
harness = Harness(HarnessConfig(
    allowed_tools={"ast_analysis", "radon", "ripgrep", "git_log"},
    call_limit_per_tool=5,
    recovery_strategy="REPLAN",
))

graph = build_agent_graph(llm=llm, harness=harness, store=store, max_iterations=10)

initial_state = AgentState(
    goal="Understand the authentication module",
    current_task="map module structure",
).model_dump()

final = graph.invoke(initial_state)

print(f"Complete: {final['complete']}")
print(f"Iterations: {final['iteration']}")
print(f"Findings: {final['findings']}")
```

### 6.5 Verify a hypothesis

```python
from archon.verification.harness import EvidenceItem, verify_hypothesis
from archon.verification.hallucination import promote_to_graph

evidence = [
    EvidenceItem(source="auth.py:14",
                 content="def hash_password(self, password: str) -> str:",
                 supports=True),
    EvidenceItem(source="auth.py:22",
                 content="def verify_password(self, password: str, stored: str) -> bool:",
                 supports=True),
]

result = verify_hypothesis("auth module handles password hashing and verification", evidence)
print(f"Status: {result.status}")         # VERIFIED
print(f"Confidence: {result.confidence}") # 0.8

# Write to graph only if provenance exists
promote_to_graph(
    claim="auth module handles password hashing",
    evidence_texts=["auth.py:14 — def hash_password"],
    store=store,
    confidence=result.confidence,
    node_id="finding::auth_hashing",
)
```

### 6.6 Save and resume sessions

```python
from archon.memory.sqlite_store import SQLiteStore
from archon.memory.redis_store import make_redis_store

# Session memory
db = SQLiteStore(db_path="./output/session.db")
db.create_session("my_session", "understand auth")
db.save_iteration("my_session", final_state)
db.save_evidence("my_session", "auth.py", "auth.py:14",
                  "def hash_password", supports=True)

# Load previous session
history = db.load_session("my_session")
evidence = db.get_evidence_for_module("auth.py")

# Cross-session summary
redis = make_redis_store()
redis.save_repo_summary("my_repo_hash", {
    "modules": 23,
    "verified_findings": 6,
    "avg_confidence": 0.82,
})
summary = redis.load_repo_summary("my_repo_hash")
```

### 6.7 Generate documentation

```python
from archon.docs.generator import DocumentationGenerator

gen = DocumentationGenerator(store=store, parse_result=parse_result)
gen.generate(
    session_id="my_session",
    output_dir="./output",
    goal="Understand the authentication module",
)
```

---

## 7. Output Files Reference

After a successful `investigate` run:

```
output/
├── report.md              ← Master investigation report
│                             Contains: summary table, verified findings
│                             with confidence scores, module list, unknowns
│
├── session.db             ← SQLite session history
│                             All iterations + evidence cache
│
├── modules/               ← Per-module documentation
│   ├── auth.py.md
│   ├── api.py.md
│   ├── models.py.md
│   └── ...
│
├── architecture.dot       ← Graphviz source for dependency graph
├── architecture.png       ← Rendered dependency graph
├── callgraph.dot          ← Graphviz source for call graph
└── callgraph.png          ← Rendered call graph
```

### report.md structure

```markdown
# Code-Archon Investigation Report

**Goal:** Understand the authentication module
**Session:** sess_a3f72b1c

## Summary
| Metric            | Value |
|-------------------|-------|
| Modules documented| 5     |
| Verified findings | 6     |
| Average confidence| 0.83  |
| Unknowns remaining| 0     |

## Verified Findings
### 1. auth module handles password hashing
- **Confidence:** 0.90
- **Provenance:** `auth.py:14`

...

## Modules
### `auth.py`
- Lines: 42 | Avg CC: 2.3 | Imports: hashlib, os

## Unknowns
*All investigation objectives met.*
```

---

## 8. Adjusting the Agent

### Tune max iterations

```bash
# Quick scan (fast, less thorough)
python -m archon.cli investigate --repo ./repo --max-iter 5

# Deep investigation (slow, more thorough)
python -m archon.cli investigate --repo ./repo --max-iter 30
```

### Restrict which tools the agent can use

Edit `archon/agent/harness.py` `HarnessConfig` defaults, or pass a custom harness via the Python API:

```python
from archon.agent.harness import Harness, HarnessConfig

# Read-only analysis only (no test execution)
harness = Harness(HarnessConfig(
    allowed_tools={"ast_analysis", "radon", "ripgrep"},
    call_limit_per_tool=3,
))
```

### Change the LLM

In `.env`:
```env
# Use Anthropic instead of Groq
LLM_PROVIDER=anthropic
ANTHROPIC_API_KEY=sk-ant-...
LLM_MODEL=claude-sonnet-4-6

# Use OpenAI
LLM_PROVIDER=openai
OPENAI_API_KEY=sk-...
LLM_MODEL=gpt-4o-mini
```

---

## 9. Running the Test Suite

```bash
# All tests
python -m pytest tests/ -v

# Specific phase
python -m pytest tests/phase1/ -v    # AST parser
python -m pytest tests/phase2/ -v    # Graph store
python -m pytest tests/phase6/ -v    # Verification

# Edge case / extended tests
python -m pytest tests/test_extended.py -v

# E2E test (uses mock LLM, no network required)
python -m pytest tests/e2e/test_e2e.py -v

# With coverage report
python -m pytest tests/ --cov=archon --cov-report=term-missing
```

---

## 10. Common Issues

### `ModuleNotFoundError: No module named 'archon'`
```bash
pip install -e .
```

### `Neo4j not running — start with: docker-compose up -d neo4j`
The system falls back to in-memory store automatically. Start Docker if you want persistence across runs.

### `LLM unavailable — heuristic mode`
Check `GROQ_API_KEY` in `.env`. The system works without LLM in `--no-llm` mode.

### `graphviz: command not found`
Install Graphviz:
```bash
# Ubuntu/Debian
sudo apt-get install graphviz

# macOS
brew install graphviz

# Without it, .dot files are generated but .png files are 1×1 placeholders
```

### `semgrep not found`
Semgrep is optional. Install with:
```bash
pip install semgrep
```
Without it, `run_semgrep()` returns `[]` gracefully.

### Tests fail with `chromadb DeprecationWarning`
This is a warning, not an error. ChromaDB will require `get_config()` on embedding functions in a future version. Does not affect functionality.

---

## 11. Architecture Quick Reference

```
archon/
├── config.py              Environment config
├── llm.py                 LLM factory (Groq/Anthropic/OpenAI)
├── goal_analyzer.py       Objective → InvestigationGoal
├── cli.py                 Typer CLI
├── ingestion/
│   └── ast_parser.py      Python AST → ModuleNode/ClassNode/FunctionNode
├── graph/
│   ├── neo4j_client.py    Graph store (Neo4j + in-memory fallback)
│   └── network_graph.py   NetworkX mirror (BFS, cycles, entry points)
├── retrieval/
│   ├── bm25.py            BM25 keyword index
│   └── vector_store.py    ChromaDB + ContextEngine
├── agent/
│   ├── loop.py            LangGraph StateGraph (8-node cycle)
│   └── harness.py         Tool permissions + call limits
├── tools/
│   ├── static.py          ast, radon, semgrep
│   ├── runtime.py         pytest, coverage
│   ├── search.py          ripgrep, ctags
│   └── git_tools.py       git log, blame, diff
├── verification/
│   ├── harness.py         VERIFIED/REFUTED/UNCERTAIN logic
│   └── hallucination.py   Provenance filter + graph gate
├── memory/
│   ├── sqlite_store.py    Session history + evidence cache
│   └── redis_store.py     Cross-session repo summaries
└── docs/
    ├── generator.py       Jinja2 + Graphviz doc generation
    └── templates/
        ├── report.md.j2
        └── module.md.j2
```
