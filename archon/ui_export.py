"""Bake an investigation and its generated artefacts into one offline dashboard."""
from __future__ import annotations

import base64
import json
import re
import sqlite3
from datetime import datetime
from pathlib import Path

from archon.agent.evidence import is_source_path

_UI = Path(__file__).parent / "ui"
_REF = re.compile(r"^(.+?):(\d+)$")


def _snippet(repo: Path, ref: str, ctx: int = 10):
    m = _REF.match(ref)
    if not m:
        return None
    rel, line = m.group(1).replace("\\", "/"), int(m.group(2))
    f = (repo / rel).resolve()
    if repo.resolve() not in f.parents or not f.is_file():
        return None
    lines = f.read_text(encoding="utf-8", errors="replace").splitlines()
    a = max(0, line - 1 - ctx)
    return {"path": rel, "start": a + 1, "hl": line, "lines": lines[a:line + ctx]}


def _read_text(path: Path, limit: int = 500_000) -> str:
    try:
        return path.read_text(encoding="utf-8", errors="replace")[:limit] if path.is_file() else ""
    except OSError:
        return ""

def _task_verification(task: str, has_verified_finding: bool, unknown_set: set[str]) -> dict[str, str]:
    """Describe verification independently from whether a task was attempted."""
    if has_verified_finding:
        status = "VERIFIED"
        detail = "A verified finding was recorded for this task."
    elif task in unknown_set:
        status = "UNRESOLVED"
        detail = "The task was attempted but no verified conclusion was established."
    else:
        status = "NOT VERIFIED"
        detail = "No verified finding was linked to this task; treat the result as unknown, not false."
    return {
        "status": status,
        "verification_label": "VERIFIED" if status == "VERIFIED" else "NOT VERIFIED",
        "status_detail": detail,
    }




def _artifact(path: Path, kind: str, title: str) -> dict:
    item = {"name": path.name, "title": title, "kind": kind, "exists": path.is_file(),
            "size": path.stat().st_size if path.is_file() else 0, "content": ""}
    if kind in {"markdown", "dot", "text"}:
        item["content"] = _read_text(path)
    elif kind == "image" and path.is_file():
        try:
            item["data"] = "data:image/png;base64," + base64.b64encode(path.read_bytes()).decode("ascii")
        except OSError:
            item["data"] = ""
    return item


def _state_history(output_dir: Path, session: str) -> list[dict]:
    """Read only this session's persisted snapshots; never infer missing intermediate states."""
    db = output_dir / "session.db"
    if not db.is_file():
        return []
    try:
        conn = sqlite3.connect(f"file:{db.as_posix()}?mode=ro", uri=True, timeout=1)
        rows = conn.execute(
            "SELECT iteration, state_snapshot, created_at FROM iteration_log "
            "WHERE session_id = ? ORDER BY id", (session,)
        ).fetchall()
        conn.close()
        result = []
        for iteration, raw, created_at in rows:
            try:
                state = json.loads(raw)
            except (TypeError, json.JSONDecodeError):
                continue
            result.append({
                "iteration": iteration, "created_at": str(created_at or ""),
                "phase": str(state.get("phase", "")),
                "current_task": state.get("current_task", ""),
                "task_index": state.get("task_index", 0),
                "tasks": state.get("tasks", []),
                "retries": state.get("retries", 0),
                "evidence_count": len(state.get("evidence", [])),
                "evidence": state.get("evidence", []),
                "hypothesis": state.get("hypothesis"),
                "last_failure": state.get("last_failure", ""),
                "search_terms": state.get("search_terms", []),
                "findings": state.get("findings", []),
                "rejected": state.get("rejected", []),
                "unknowns": state.get("unknowns", []),
                "tool_calls": state.get("tool_calls", []),
                "complete": state.get("complete", False),
                "error": state.get("error"),
            })
        return result
    except (sqlite3.Error, OSError):
        return []


def build_ui(store, parse_result, final, repo, goal, session, mode, out_path) -> Path:
    repo = Path(repo).resolve()
    out = Path(out_path)
    output_dir = out.parent
    nodes = store.all_nodes()
    edges = store.all_edges()
    ev = {n.id: n for n in nodes if n.label == "Evidence"}
    findings = []
    sources = {}
    for h in sorted((n for n in nodes if n.label == "Hypothesis"), key=lambda n: n.id):
        refs = [ev[e.source_id] for e in edges if e.rel_type == "SUPPORTS" and e.target_id == h.id
                and e.source_id in ev]
        mods = sorted({e.target_id for e in edges if e.rel_type == "ABOUT" and e.source_id == h.id})
        evidence = [{"source": x.provenance, "tool": x.properties.get("tool", ""),
                     "content": x.properties.get("content", "")} for x in refs]
        for ref in [h.provenance] + [x["source"] for x in evidence]:
            if ref and ref not in sources and (snippet := _snippet(repo, ref)):
                sources[ref] = snippet
        findings.append({"id": h.id, "task": h.properties.get("task", ""),
                         "claim": h.properties.get("claim", h.id), "confidence": h.confidence,
                         "provenance": h.provenance, "evidence": evidence, "modules": mods})
    cited = {m for finding in findings for m in finding["modules"]}
    modules = [m for m in parse_result.modules if is_source_path(m.id)] or parse_result.modules
    module_ids = {m.id for m in modules}
    function_count = {}
    for fn in parse_result.functions:
        function_count[fn.module_path] = function_count.get(fn.module_path, 0) + 1

    module_data = []
    for m in parse_result.modules:
        module_data.append({
            "id": m.id, "path": getattr(m, "path", m.id), "docstring": getattr(m, "docstring", "") or "",
            "imports": list(getattr(m, "imports", []) or []),
            "external_deps": list(getattr(m, "external_deps", []) or []),
            "lines": int(getattr(m, "line_count", 0) or 0),
            "avg_complexity": float(getattr(m, "avg_complexity", 0) or 0),
            "functions": function_count.get(m.id, 0),
            "cited": m.id in cited,
        })
    function_data = []
    for fn in parse_result.functions:
        function_data.append({
            "id": f"{fn.module_path}::{fn.name}", "name": fn.name, "module": fn.module_path,
            "class_name": getattr(fn, "class_name", "") or "",
            "args": list(getattr(fn, "args", []) or []),
            "return_type": getattr(fn, "return_type", "") or "",
            "docstring": getattr(fn, "docstring", "") or "",
            "calls": list(getattr(fn, "calls", []) or []),
            "complexity": float(getattr(fn, "complexity", 0) or 0),
            "start_line": int(getattr(fn, "start_line", 0) or 0),
            "end_line": int(getattr(fn, "end_line", 0) or 0),
        })
    class_data = []
    for cls in parse_result.classes:
        class_data.append({
            "id": f"{cls.module_path}::{cls.name}", "name": cls.name, "module": cls.module_path,
            "bases": list(getattr(cls, "bases", []) or []),
            "docstring": getattr(cls, "docstring", "") or "",
            "methods": list(getattr(cls, "methods", []) or []),
            "start_line": int(getattr(cls, "start_line", 0) or 0),
            "end_line": int(getattr(cls, "end_line", 0) or 0),
        })

    # Embed focused source windows for the code explorer as well as findings.
    # This keeps the generated dashboard useful offline without copying entire repositories.
    for ref in [m["id"] + ":1" for m in module_data] + [
        item["module"] + ":" + str(item["start_line"])
        for item in function_data + class_data if item.get("start_line")
    ]:
        if ref not in sources and (snippet := _snippet(repo, ref)):
            sources[ref] = snippet

    relation_counts = {}
    for edge in edges:
        relation_counts[edge.rel_type] = relation_counts.get(edge.rel_type, 0) + 1
    graph_nodes = [{
        "id": n.id, "label": n.label, "confidence": float(n.confidence),
        "provenance": n.provenance, "properties": n.properties, "cited": n.id in cited,
    } for n in nodes]
    graph_edges = [{"source": e.source_id, "target": e.target_id, "type": e.rel_type,
                    "properties": e.properties} for e in edges]

    history = _state_history(output_dir, session)
    latest = history[-1] if history else {}
    state_evidence = latest.get("evidence", []) if latest else final.get("evidence", [])
    evidence_items = []
    seen_evidence = set()
    for item in list(state_evidence or []) + [
        {"source": n.provenance, "tool": n.properties.get("tool", ""),
         "content": n.properties.get("content", ""), "supports": True}
        for n in nodes if n.label == "Evidence"
    ]:
        if hasattr(item, "model_dump"):
            item = item.model_dump()
        if not isinstance(item, dict):
            continue
        source = str(item.get("source", item.get("provenance", "")) or "")
        content = str(item.get("content", "") or "")
        tool = str(item.get("tool", "") or "")
        key = (source, content, tool)
        if key in seen_evidence:
            continue
        seen_evidence.add(key)
        if source and source not in sources and (snippet := _snippet(repo, source)):
            sources[source] = snippet
        evidence_items.append({"source": source, "content": content, "tool": tool,
                               "supports": item.get("supports", None)})

    tasks = []
    all_tasks = list(final.get("tasks", []) or [])
    unknown_set = set(final.get("unknowns", []) or [])
    not_verified = []
    for i, task in enumerate(all_tasks):
        matched = [finding for finding in findings if finding["task"] == task]
        verification = _task_verification(task, bool(matched), unknown_set)
        status = verification["status"]
        task_row = {"index": i + 1, "task": task, **verification,
                    "finding_ids": [f["id"] for f in matched]}
        tasks.append(task_row)
        if status == "NOT VERIFIED":
            not_verified.append({"task": task, "status": status, "reason": task_row["status_detail"],
                                 "evidence_count": 0})
    # Keep a final in-flight hypothesis visible if it was not promoted to a verified graph finding.
    hypothesis = final.get("hypothesis")
    if hasattr(hypothesis, "model_dump"):
        hypothesis = hypothesis.model_dump()
    if isinstance(hypothesis, dict):
        claim = str(hypothesis.get("claim", "") or "").strip()
        hstatus = str(hypothesis.get("status", "PENDING") or "PENDING").upper()
        if claim and hstatus != "VERIFIED" and claim not in unknown_set and not any(x["task"] == claim for x in not_verified):
            not_verified.append({"task": claim, "status": hstatus,
                                 "reason": "This hypothesis was not promoted as a verified finding.",
                                 "evidence_count": len(hypothesis.get("evidence", []) or [])})

    artifact_list = [
        _artifact(output_dir / "report.md", "markdown", "Investigation report"),
        _artifact(output_dir / "architecture.png", "image", "Module dependency map"),
        _artifact(output_dir / "callgraph.png", "image", "Function call graph"),
        _artifact(output_dir / "architecture.dot", "dot", "Architecture graph source"),
        _artifact(output_dir / "callgraph.dot", "dot", "Call graph source"),
    ]
    module_docs = sorted((output_dir / "modules").glob("*.md")) if (output_dir / "modules").is_dir() else []
    artifact_list.extend(_artifact(p, "markdown", p.stem.replace("_", " / ")) for p in module_docs)
    count = lambda relation: relation_counts.get(relation, 0)
    data = {
        "meta": {"repo": repo.name, "repo_path": str(repo), "goal": goal, "session": session, "mode": mode,
                 "generated": datetime.now().strftime("%Y-%m-%d %H:%M"), "complete": bool(final.get("complete", False))},
        "stats": {"modules": len(parse_result.modules), "functions": len(parse_result.functions),
                  "classes": len(parse_result.classes), "calls": count("CALLS"),
                  "imports": count("IMPORTS"), "inherits": count("INHERITS"), "contains": count("CONTAINS"),
                  "findings": len(findings), "blocked": len(final.get("rejected", [])),
                  "not_verified": len(not_verified), "unresolved": len(final.get("unknowns", [])), "parse_errors": len(parse_result.errors),
                  "evidence": len(evidence_items), "graph_nodes": len(nodes), "graph_edges": len(edges),
                  "external_deps": len({d for m in module_data for d in m["external_deps"]}),
                  "iterations": int(final.get("iteration", 0) or 0)},
        "findings": findings, "unknowns": list(final.get("unknowns", []) or []),
        "not_verified": not_verified, "rejected": list(final.get("rejected", []) or []), "tasks": tasks,
        "agent": {"phase": str(final.get("phase", "")), "iteration": final.get("iteration", 0),
                  "task_index": final.get("task_index", 0), "current_task": final.get("current_task", ""),
                  "retries": final.get("retries", 0), "last_failure": final.get("last_failure", ""),
                  "search_terms": list(final.get("search_terms", []) or []), "error": final.get("error"),
                  "complete": final.get("complete", False), "tool_calls": list(final.get("tool_calls", []) or [])},
        "history": history, "evidence": evidence_items, "modules": module_data,
        "functions": function_data, "classes": class_data, "parse_errors": list(parse_result.errors),
        "graph": {"nodes": graph_nodes, "edges": graph_edges,
                  "dependency_nodes": [{"id": m.id, "lines": m.line_count, "fns": function_count.get(m.id, 0),
                                        "cited": m.id in cited} for m in modules],
                  "dependency_edges": [[e.source_id, e.target_id] for e in edges
                                       if e.rel_type == "IMPORTS" and e.source_id in module_ids and e.target_id in module_ids]},
        "sources": sources, "artifacts": artifact_list,
        "external_deps": sorted({d for m in module_data for d in m["external_deps"]}),
    }
    html = (_UI / "template.html").read_text(encoding="utf-8")
    cy = _UI / "cytoscape.min.js"
    html = html.replace("/*__CYTOSCAPE__*/", cy.read_text(encoding="utf-8") if cy.exists() else "")
    html = html.replace("/*__DATA__*/null", json.dumps(data, default=str).replace("</", "<\\/"))
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(html, encoding="utf-8")
    return out


