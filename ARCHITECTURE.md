# Code-Archon — Architecture Document

**Current Implementation vs. Synopsis Specification**

---

## 1. Synopsis Architecture (from PDF)

The synopsis described a layered architecture with the following components:

```
Legacy Repository
       │
  Goal Analyzer
       │
  Agent Loop (LangGraph / CrewAI)
  Plan → Act → Observe → Verify
       │
    Harness (rules, permissions, stop criteria)
       │
  Context Engine (BM25 + ChromaDB/pgvector)
       │
  ┌────────────┬──────────────┬─────────────────┐
  │  Static    │  Runtime+Git │  Filesystem+    │
  │  Analysis  │  (pytest,    │  Search         │
  │  (ast,     │  coverage,   │  (ripgrep,      │
  │  radon,    │  gitpython,  │  ctags, grep)   │
  │  semgrep,  │  Docker)     │                 │
  │  tree-sitter)             │                 │
  └────────────┴──────────────┴─────────────────┘
       │
  Context/Knowledge Graph (Neo4j + NetworkX)
  Nodes: Modules, Classes, Functions, APIs,
         Behaviors, Hypotheses, Evidence, Gaps
       │
  Memory Layer (SQLite + Redis + Embeddings)
       │
  Verification Harness
  (pytest re-run, static cross-check,
   hallucination filter — file:line provenance)
       │
  Documentation Generator
  (Jinja2, Sphinx, Graphviz, D3.js)
       │
  Output: Architecture map, dependency graph,
          annotated docs, detected bugs
```

**Specified LLMs:** GPT-4o or Claude 3.7 Sonnet
**Specified agent framework:** LangGraph or CrewAI
**Specified tool interface:** MCP (Model Context Protocol)

---

## 2. Current Implementation Architecture

```
Legacy Repository (.py files)
          │
          ▼
┌─────────────────────────────────────┐
│  archon/ingestion/ast_parser.py     │  ← Phase 1
│  parse_repository(repo_root)        │
│  → ModuleNode, ClassNode,           │
│    FunctionNode (Pydantic)          │
│  Tools: ast, radon, tomllib        │
└────────────────┬────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────┐
│  archon/graph/                      │  ← Phase 2
│  ├── neo4j_client.py               │
│  │   make_graph_store()            │
│  │   _Neo4jStore  (production)     │
│  │   _InMemoryStore (fallback)     │
│  │   Labels: Module, Class,        │
│  │   Function, Hypothesis,Evidence │
│  │   Edges: IMPORTS, CALLS,        │
│  │   INHERITS, CONTAINS, SUPPORTS  │
│  │   Every node: confidence+provenance│
│  └── network_graph.py              │
│      ArchonGraph (NetworkX DiGraph)│
│      find_entry_points()           │
│      find_dead_code()              │
│      get_call_chain() [BFS]        │
│      has_cycle() / find_cycles()   │
└────────────────┬────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────┐
│  archon/retrieval/                  │  ← Phase 3
│  ├── bm25.py  BM25Index            │
│  │   rank-bm25, keyword search     │
│  └── vector_store.py               │
│      VectorStore (ChromaDB)        │
│      _HashEmbeddingFunction (CI)   │
│      DefaultEmbeddingFunction (prod│
│      ContextEngine:                │
│        query() → hybrid BM25+vec  │
│        build_context_window()      │
│        chunks_from_parse_result()  │
└────────────────┬────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────┐
│  archon/goal_analyzer.py            │  ← Phase 4
│  GoalAnalyzer                       │
│  ├── _keyword_analyze() (offline)  │
│  └── _llm_analyze() (Groq/LLM)    │
│  → InvestigationGoal               │
│    (objective, focus_modules,      │
│     investigation_tasks,           │
│     success_criteria)              │
└────────────────┬────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────┐
│  archon/agent/                      │  ← Phase 4-5
│  ├── loop.py  LangGraph StateGraph │
│  │   Nodes: plan, act, observe,    │
│  │   verify, update_graph,         │
│  │   identify_unknowns,            │
│  │   investigate, complete         │
│  │   AgentState (Pydantic)         │
│  │   Hard stop in node_plan()      │
│  └── harness.py  Harness           │
│      ToolNotPermittedError         │
│      ToolCallLimitError            │
│      allowed_tools allowlist       │
│      call_limit_per_tool           │
│      recovery_strategy             │
│      Full call log                 │
└────────────────┬────────────────────┘
                 │
       ┌─────────┼─────────┐
       ▼         ▼         ▼
  archon/tools/
  ├── static.py            (ast, radon, semgrep)
  ├── runtime.py           (pytest, coverage.py)
  ├── search.py            (ripgrep → grep fallback)
  └── git_tools.py         (gitpython: log, blame, diff)
       │
       ▼
┌─────────────────────────────────────┐
│  archon/verification/               │  ← Phase 6
│  ├── harness.py                    │
│  │   verify_hypothesis()           │
│  │   VerificationStatus:           │
│  │   VERIFIED / REFUTED / UNCERTAIN│
│  │   Confidence: 0.5+0.15×n ≤0.95 │
│  └── hallucination.py              │
│      check_claim()                 │
│      regex: [\w/\\.-]+\.py:\d+    │
│      promote_to_graph()            │
│      — blocked if HALLUCINATED     │
└────────────────┬────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────┐
│  archon/memory/                     │  ← Phase 7
│  ├── sqlite_store.py SQLiteStore   │
│  │   Tables: sessions,             │
│  │   iteration_log, evidence_cache │
│  └── redis_store.py RedisStore     │
│      Key: archon:repo:{hash}:summary│
│      TTL: 30 days                  │
│      _MockRedisStore (fallback)    │
└────────────────┬────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────┐
│  archon/docs/generator.py           │  ← Phase 8
│  DocumentationGenerator            │
│  Outputs:                          │
│  ├── report.md  (Jinja2)           │
│  ├── modules/*.md (per-module)     │
│  ├── architecture.dot + .png       │
│  └── callgraph.dot + .png          │
└─────────────────────────────────────┘
          │
          ▼
   archon/cli.py
   archon investigate --repo ./path --goal "..."
```

---

## 3. Component-by-Component Comparison

### 3.1 Goal Analyzer

| Aspect | Synopsis Spec | Current Implementation |
|--------|--------------|----------------------|
| Input | Free-text objective | Free-text objective ✅ |
| Output | Investigation goal + tasks | `InvestigationGoal` Pydantic model ✅ |
| LLM-backed | GPT-4o / Claude 3.7 | Groq llama-3.3-70b-versatile ✅ (swappable) |
| Offline fallback | Not specified | Keyword-based `_keyword_analyze()` ✅ |

### 3.2 Agent Loop

| Aspect | Synopsis Spec | Current Implementation |
|--------|--------------|----------------------|
| Framework | LangGraph or CrewAI | LangGraph `StateGraph` ✅ |
| Cycle | Plan→Act→Observe→Verify | PLAN→ACT→OBSERVE→VERIFY→UPDATE_GRAPH→IDENTIFY_UNKNOWNS ✅ |
| LLM driver | GPT-4o / Claude 3.7 | Groq (via `make_llm()`) ✅ |
| Recovery | "Revise, retry, replan" | INVESTIGATE node → loops to PLAN ✅ |
| Hard stop | Not specified | `max_iterations` in `node_plan()` ✅ |
| State schema | Not specified | `AgentState` Pydantic model ✅ |

### 3.3 Harness

| Aspect | Synopsis Spec | Current Implementation |
|--------|--------------|----------------------|
| Tool permissions | Allowlist per goal type | `HarnessConfig.allowed_tools` set ✅ |
| Call limits | Per-tool max calls | `call_limit_per_tool` enforced ✅ |
| Require evidence | Before promoting claims | `require_evidence_before_promote` flag ✅ |
| Recovery strategies | Not detailed | REPLAN / RETRY / SKIP configurable ✅ |
| Logging | Not specified | Full `ToolCall` log per session ✅ |

### 3.4 Context Engine

| Aspect | Synopsis Spec | Current Implementation |
|--------|--------------|----------------------|
| BM25 | `rank-bm25` | `BM25Index` using `rank-bm25` ✅ |
| Vector store | ChromaDB or pgvector | ChromaDB ✅ |
| Embeddings | sentence-transformers or OpenAI | Hash embed (CI) / MiniLM (prod) ✅ |
| Sliding window | Specified | `build_context_window()` token budget ✅ |

### 3.5 Context / Knowledge Graph

| Aspect | Synopsis Spec | Current Implementation |
|--------|--------------|----------------------|
| Graph DB | Neo4j (AuraDB / Community) | Neo4j + `_InMemoryStore` fallback ✅ |
| Query language | Cypher | Cypher in `_Neo4jStore` ✅ |
| In-process | NetworkX | `ArchonGraph` (NetworkX DiGraph) ✅ |
| Node types | modules, classes, functions, APIs, behaviors, hypotheses, evidence | Module, Class, Function, Hypothesis, Evidence ✅ (APIs, behaviors deferred to Phase 9+) |
| Edge types | imports, calls, inheritance, data flow, evidence-to-claim | IMPORTS, CALLS, INHERITS, CONTAINS, SUPPORTS ✅ |
| Confidence scores | Per node | `confidence: float` on every node ✅ |
| Provenance | File:line per node | `provenance: str` on every node ✅ |
| Cycle detection | Not explicitly specified | `has_cycle()`, `find_cycles()` ✅ |

### 3.6 Tool Layer

| Tool | Synopsis Spec | Current Implementation |
|------|--------------|----------------------|
| AST analysis | `ast`, `jedi`, `rope` | `ast` (full), `jedi` (stub) ✅ |
| Complexity | `radon`, `pylint`, `mypy` | `radon` ✅ (pylint/mypy deferred) |
| Security | `semgrep`, `tree-sitter` | `semgrep` (subprocess) ✅ |
| Tests | `pytest`, `coverage.py`, `hypothesis` | `pytest` + `coverage.py` ✅ |
| Git | `gitpython`, `PyGit2` | `gitpython` ✅ |
| Search | `ripgrep`, `ctags` | `ripgrep` (+ grep fallback) ✅, `ctags` ✅ |
| Docker sandbox | Specified | Not yet implemented ⚠️ |
| MCP interface | Specified | Not yet implemented ⚠️ |

### 3.7 Verification Harness

| Aspect | Synopsis Spec | Current Implementation |
|--------|--------------|----------------------|
| pytest re-run | Specified | `run_pytest()` available ✅ |
| Static cross-check | Specified | Radon + semgrep cross-check ✅ |
| Hallucination filter | Claims must trace to file:line | `check_claim()` + `promote_to_graph()` ✅ |
| Confidence promotion | Not detailed | `confidence = min(0.5 + 0.15×n, 0.95)` ✅ |

### 3.8 Memory Layer

| Aspect | Synopsis Spec | Current Implementation |
|--------|--------------|----------------------|
| Session memory | SQLite | `SQLiteStore` (3-table schema) ✅ |
| Cross-session | Redis | `RedisStore` + `_MockRedisStore` fallback ✅ |
| Embedding cache | Specified | Deferred (ChromaDB acts as cache) ⚠️ |

### 3.9 Documentation Generator

| Aspect | Synopsis Spec | Current Implementation |
|--------|--------------|----------------------|
| Templates | Jinja2 | Jinja2 `.j2` templates ✅ |
| API docs | Sphinx | Deferred ⚠️ |
| Diagrams | Graphviz, D3.js | Graphviz `.dot` → `.png` ✅, D3.js deferred ⚠️ |
| Reports | Markdown / HTML | Markdown ✅, HTML deferred ⚠️ |

### 3.10 LLM Provider

| Aspect | Synopsis Spec | Current Implementation |
|--------|--------------|----------------------|
| Primary LLM | GPT-4o or Claude 3.7 Sonnet | Groq llama-3.3-70b-versatile ✅ |
| Rationale | Paid API, high capability | Free tier, fast, sufficient for structured tasks |
| Fallback | Not specified | Keyword-only mode (no LLM needed) ✅ |
| Swappable | Not specified | `make_llm()` factory supports Groq/Anthropic/OpenAI ✅ |

---

## 4. What Is Deferred / Not Yet Implemented

These items are in the synopsis spec but not yet in the current implementation:

| Feature | Reason |
|---------|--------|
| Docker sandbox for runtime tool execution | Adds complexity; subprocess isolation used instead |
| MCP (Model Context Protocol) tool interface | Would replace current tool layer in Phase 10+ |
| Sphinx API documentation | Phase 10 deliverable |
| D3.js interactive dependency graph | Frontend phase, post-core |
| `jedi`, `rope`, `pylint`, `mypy` deep integration | Radon + semgrep cover core analysis |
| `hypothesis` (fuzz testing) | Runtime phase, post-core |
| `pgvector` as vector store | ChromaDB sufficient; pgvector for scaling |
| `PyGit2` | gitpython covers all needed operations |
| Embedding cache (separate from vector store) | ChromaDB upsert acts as cache |
| CrewAI multi-agent option | LangGraph selected as primary |

---

## 5. Data Flow — End to End

```
User: archon investigate --repo ./legacy --goal "understand auth"

1. CLI parses args
2. ast_parser.parse_repository(./legacy)
   → [ModuleNode, ClassNode, FunctionNode, ...]

3. GraphStore.upsert_node() for each node
   → Neo4j (or _InMemoryStore)
   → ArchonGraph.sync_from_store()

4. BM25Index.build(chunks)
   VectorStore.add_chunks(chunks)

5. GoalAnalyzer.analyze("understand auth")
   → InvestigationGoal(tasks=[...])

6. build_agent_graph(llm, harness, store)
   graph.invoke(AgentState(goal=...).model_dump())

   Loop (up to max_iterations):
     PLAN:           form hypothesis
     ACT:            harness.execute_default_tool()
     OBSERVE:        collect evidence
     VERIFY:         llm.invoke() or heuristic
       → VERIFIED:   update_graph → identify_unknowns
       → UNCERTAIN:  investigate → replan
     IDENTIFY_UNKNOWNS: store.low_confidence_nodes()
     COMPLETE:       break

7. SQLiteStore.save_iteration(session_id, final_state)

8. DocumentationGenerator.generate(session_id, ./output)
   → output/report.md
   → output/modules/auth.py.md
   → output/architecture.dot/.png
   → output/callgraph.dot/.png
```

---

## 6. Key Architectural Decisions

### In-Memory Fallbacks Everywhere
Every external service has a same-interface in-memory fallback:
- Neo4j → `_InMemoryStore`
- Redis → `_MockRedisStore`
- MiniLM embeddings → `_HashEmbeddingFunction`

This means the entire stack runs without any Docker or external services, which is critical for CI and development.

### Hallucination Filter as Hard Gate
The hallucination filter (`promote_to_graph()`) is a hard write gate — no claim can enter the knowledge graph without a `file.py:line` provenance reference. This is the core academic contribution: provenance-enforced knowledge.

### LangGraph Dict Wrapping
LangGraph's `StateGraph(dict)` requires plain dicts. Pydantic `AgentState` models are wrapped/unwrapped at every node boundary:
```python
def wrap(fn):
    def _wrapped(state_dict):
        s = AgentState(**state_dict)
        return fn(s).model_dump()
    return _wrapped
```
This keeps node functions type-safe internally while satisfying LangGraph's dict contract.

### UUID-per-VectorStore Collection
ChromaDB `EphemeralClient` is a process-level singleton. Every `VectorStore` instance gets a unique collection name to prevent cross-instance data contamination in tests.
