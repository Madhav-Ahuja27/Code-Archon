"""Bake an investigation into one self-contained, offline index.html dashboard."""
from __future__ import annotations

import json
import re
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
    if repo.resolve() not in f.parents or not f.is_file():   # no path traversal
        return None
    lines = f.read_text(encoding="utf-8", errors="replace").splitlines()
    a = max(0, line - 1 - ctx)
    return {"path": rel, "start": a + 1, "hl": line, "lines": lines[a:line + ctx]}


def build_ui(store, parse_result, final, repo, goal, session, mode, out_path) -> Path:
    repo = Path(repo)
    nodes = store.all_nodes()
    edges = store.all_edges()
    ev = {n.id: n for n in nodes if n.label == "Evidence"}
    findings, sources = [], {}
    for h in sorted((n for n in nodes if n.label == "Hypothesis"), key=lambda n: n.id):
        refs = [ev[e.source_id] for e in edges if e.rel_type == "SUPPORTS" and e.target_id == h.id
                and e.source_id in ev]
        mods = sorted({e.target_id for e in edges if e.rel_type == "ABOUT" and e.source_id == h.id})
        r = [{"source": x.provenance, "tool": x.properties.get("tool", ""),
              "content": x.properties.get("content", "")} for x in refs]
        for ref in [h.provenance] + [x["source"] for x in r]:
            if ref not in sources and (s := _snippet(repo, ref)):
                sources[ref] = s
        findings.append({"task": h.properties.get("task", ""), "claim": h.properties.get("claim", ""),
                         "confidence": h.confidence, "provenance": h.provenance,
                         "evidence": r, "modules": mods})
    cited = {m for f in findings for m in f["modules"]}
    mods = [m for m in parse_result.modules if is_source_path(m.id)] or parse_result.modules
    ids = {m.id for m in mods}
    nfn = {}
    for fn in parse_result.functions:
        nfn[fn.module_path] = nfn.get(fn.module_path, 0) + 1
    count = lambda t: sum(1 for e in edges if e.rel_type == t)
    data = {
        "meta": {"repo": repo.name, "goal": goal, "session": session, "mode": mode,
                 "generated": datetime.now().strftime("%Y-%m-%d %H:%M")},
        "stats": {"modules": len(parse_result.modules), "functions": len(parse_result.functions),
                  "classes": len(parse_result.classes), "calls": count("CALLS"),
                  "imports": count("IMPORTS"), "findings": len(findings),
                  "blocked": len(final.get("rejected", [])), "unresolved": len(final.get("unknowns", []))},
        "findings": findings, "unknowns": final.get("unknowns", []),
        "graph": {"nodes": [{"id": m.id, "lines": m.line_count, "fns": nfn.get(m.id, 0),
                             "cited": m.id in cited} for m in mods],
                  "edges": [[e.source_id, e.target_id] for e in edges
                            if e.rel_type == "IMPORTS" and e.source_id in ids and e.target_id in ids]},
        "sources": sources,
    }
    html = (_UI / "template.html").read_text(encoding="utf-8")
    cy = _UI / "cytoscape.min.js"
    html = html.replace("/*__CYTOSCAPE__*/", cy.read_text(encoding="utf-8") if cy.exists() else "")
    html = html.replace("/*__DATA__*/null", json.dumps(data).replace("</", "<\\/"))
    out = Path(out_path)
    out.write_text(html, encoding="utf-8")
    return out
