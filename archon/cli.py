"""Code-Archon CLI — investigate, resume, generate-docs."""

from __future__ import annotations

import logging
import sys
import uuid
from pathlib import Path

# Keep Rich output safe in Windows consoles with legacy code pages.
for stream in (sys.stdout, sys.stderr):
    if hasattr(stream, "reconfigure"):
        stream.reconfigure(encoding="utf-8", errors="replace")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)

try:
    import typer
    from rich.console import Console
    from rich.panel import Panel
    from rich.progress import Progress, SpinnerColumn, TextColumn
except ImportError:
    print("Install typer and rich: pip install typer rich")
    sys.exit(1)

logging.getLogger("neo4j.notifications").setLevel(logging.ERROR)
logging.getLogger("httpx").setLevel(logging.WARNING)

app = typer.Typer(name="archon", help="AI Archaeologist — reverse-engineer legacy repos")
console = Console()


@app.command()
def investigate(
    repo: Path = typer.Argument(..., help="Path to the legacy repository"),
    goal: str = typer.Option("Understand the codebase architecture",
                              "--goal", "-g", help="Investigation objective"),
    output: Path = typer.Option(Path("./output"), "--output", "-o"),
    max_iter: int = typer.Option(15, "--max-iter", "-n"),
    task: list[str] = typer.Option(None, "--task", "-t",
                                   help="Investigation task (repeatable). Skips LLM decomposition."),
    session_id: str = typer.Option("", "--session-id"),
    keep_graph: bool = typer.Option(False, "--keep-graph",
                                    help="Do not wipe the existing Neo4j graph first"),
    use_llm: bool = typer.Option(True, "--llm/--no-llm",
                                  help="Use LLM (Groq) or keyword-only mode"),
):
    """Run a full investigation on a Python repository."""
    if not repo.exists():
        console.print(f"[red]Repo not found: {repo}[/red]")
        raise typer.Exit(1)

    output.mkdir(parents=True, exist_ok=True)
    sid = session_id or f"sess_{uuid.uuid4().hex[:8]}"
    console.print(Panel(
        f"[bold]Code-Archon[/bold] — AI Archaeologist\n"
        f"Repo: {repo}\nGoal: {goal}\nSession: {sid}",
        title="Investigation Start",
    ))

    # ── Phase 1: Parse repo ──────────────────────────────────────────────────
    from archon.ingestion.ast_parser import parse_repository
    from archon.graph.neo4j_client import make_graph_store, GraphNode
    from archon.graph.network_graph import ArchonGraph
    from archon.retrieval.bm25 import BM25Index
    from archon.retrieval.vector_store import VectorStore, ContextEngine
    from archon.agent.harness import Harness, HarnessConfig
    from archon.agent.loop import AgentState, build_agent_graph
    from archon.goal_analyzer import make_goal_analyzer
    from archon.memory.sqlite_store import SQLiteStore
    from archon.docs.generator import DocumentationGenerator

    with Progress(SpinnerColumn(), TextColumn("{task.description}"),
                  transient=True) as prog:

        # Parse
        t = prog.add_task("Parsing repository...")
        parse_result = parse_repository(repo)
        prog.update(t, description=(
            f"Parsed {len(parse_result.modules)} modules, "
            f"{len(parse_result.functions)} functions"
        ))
        prog.stop()

    console.print(f"[green]✓[/green] Parsed: {len(parse_result.modules)} modules, "
                  f"{len(parse_result.functions)} functions, "
                  f"{len(parse_result.errors)} errors")

    # ── Phase 2: Build graph ─────────────────────────────────────────────────
    store = make_graph_store(wait=45)  # Neo4j if available (waits while it boots), else in-memory
    if type(store).__name__ == "_Neo4jStore":
        console.print("[green]✓[/green] Graph store: Neo4j  (browse at http://localhost:7474)")
    else:
        console.print("[yellow]⚠[/yellow] Graph store: in-memory  (Neo4j not reachable; "
                      "graph will not be persisted or browsable)")
    if not keep_graph:
        store.clear()   # one graph per run; avoids mixing repos in Neo4j
    nx_graph = ArchonGraph()

    from archon.graph.builder import build_graph
    counts = build_graph(parse_result, store)
    console.print(f"[green]✓[/green] Edges: {counts.get('calls', 0)} calls, "
                  f"{counts.get('imports', 0)} imports, "
                  f"{counts.get('inherits', 0)} inherits")

    nx_graph.sync_from_store(store)
    console.print(f"[green]✓[/green] Graph: {store.node_count()} nodes")

    # ── Phase 3: Build retrieval index ───────────────────────────────────────
    chunks = ContextEngine.chunks_from_parse_result(parse_result)
    bm25 = BM25Index()
    bm25.build(chunks)
    vs = VectorStore(use_hash_embed=True)
    vs.add_chunks(chunks)
    ctx_engine = ContextEngine(bm25, vs)
    console.print(f"[green]✓[/green] Index: {len(chunks)} chunks  (vector backend: {vs.backend})")

    # ── Phase 4: Goal analysis ───────────────────────────────────────────────
    from archon.goal_analyzer import InvestigationGoal
    from archon.repo_summary import summarize_repo
    repo_summary = summarize_repo(parse_result)
    if task:
        inv_goal = InvestigationGoal(objective=goal, investigation_tasks=list(task))
    else:
        analyzer = make_goal_analyzer(use_llm=use_llm)
        inv_goal = analyzer.analyze(goal, repo_summary)
    console.print(f"[green]✓[/green] Goal decomposed into "
                  f"{len(inv_goal.investigation_tasks)} tasks")
    for task in inv_goal.investigation_tasks:
        console.print(f"  • {task}")

    # ── Phase 5-6: Agent loop ────────────────────────────────────────────────
    llm = None
    if use_llm:
        try:
            from archon.llm import make_llm
            llm = make_llm()
            console.print("[green]✓[/green] LLM connected")
        except Exception as e:
            console.print(f"[yellow]⚠[/yellow] LLM unavailable ({e}) — heuristic mode")

    harness = Harness(HarnessConfig(
        allowed_tools={"ast_analysis", "radon", "ripgrep", "git_log", "pytest"},
        call_limit_per_tool=5,
    ))

    graph = build_agent_graph(llm=llm, harness=harness, store=store,
                              max_iterations=max_iter,
                              ctx_engine=ctx_engine, repo_root=repo,
                              repo_summary=repo_summary)

    init_state = AgentState(
        goal=goal,
        tasks=list(inv_goal.investigation_tasks) or [goal],
    ).model_dump()

    console.print("\n[bold]Running agent loop...[/bold]")
    final = graph.invoke(init_state)

    console.print(f"\n[green]✓[/green] Complete after {final['iteration']} iterations")
    console.print(f"  Verified findings : {len(final['findings'])}")
    console.print(f"  Blocked by gate   : {len(final['rejected'])}  (claims citing sources not in evidence)")
    console.print(f"  Unresolved tasks  : {len(final['unknowns'])}")
    for t in final["unknowns"]:
        console.print(f"    [yellow]•[/yellow] {t}")

    # ── Phase 7: Save session ─────────────────────────────────────────────────
    db = SQLiteStore(db_path=output / "session.db")
    db.create_session(sid, goal)
    db.save_iteration(sid, final)

    # ── Phase 8: Generate docs ────────────────────────────────────────────────
    gen = DocumentationGenerator(store, parse_result)
    out_path = gen.generate(sid, output, goal=goal, unknowns=final["unknowns"])
    from archon.ui_export import build_ui
    ui_path = build_ui(store, parse_result, final, repo, goal, sid,
                       "llm" if llm else "heuristic", out_path / "index.html")
    console.print(f"[bold cyan]Dashboard → {ui_path}[/bold cyan]  (open in any browser)")

    console.print(f"\n[bold green]Documentation written → {out_path}[/bold green]")
    console.print(f"  • {out_path}/report.md")
    console.print(f"  • {out_path}/modules/  ({len(parse_result.modules)} files)")
    console.print(f"  • {out_path}/architecture.png")
    console.print(f"  • {out_path}/callgraph.png")


@app.command()
def generate_docs(
    session_id: str = typer.Argument(...),
    output: Path = typer.Option(Path("./output"), "--output", "-o"),
):
    """Regenerate docs from an existing session graph."""
    console.print(f"Generating docs for session: {session_id}")
    from archon.graph.neo4j_client import make_graph_store
    from archon.docs.generator import DocumentationGenerator
    store = make_graph_store()
    gen = DocumentationGenerator(store)
    gen.generate(session_id, output)
    console.print(f"[green]✓[/green] Docs written to {output}")


if __name__ == "__main__":
    app()
