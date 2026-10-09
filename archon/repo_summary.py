"""Compact, factual repository summary used to ground the LLM's goal decomposition
and search-term suggestions (so it knows this is, e.g., a Python Flask codebase)."""

from __future__ import annotations

from archon.agent.evidence import is_source_path


def summarize_repo(parse_result, max_modules: int = 20, max_classes: int = 15) -> str:
    mods = [m for m in parse_result.modules if is_source_path(m.id)] or list(parse_result.modules)
    classes = [c for c in parse_result.classes if is_source_path(c.module_path)] \
        or list(parse_result.classes)
    funcs = [f for f in parse_result.functions if is_source_path(f.module_path)] \
        or list(parse_result.functions)

    mods_sorted = sorted(mods, key=lambda m: -m.line_count)
    classes_sorted = sorted(classes, key=lambda c: -len(c.methods))
    dirs = sorted({m.id.rsplit("/", 1)[0] if "/" in m.id else "." for m in mods})

    lines = [
        f"Language: Python. {len(mods)} source modules, {len(funcs)} functions, "
        f"{len(classes)} classes (tests/docs/examples excluded).",
        "Source directories: " + ", ".join(dirs[:8]),
        "Largest modules: " + ", ".join(f"{m.id} ({m.line_count} lines)"
                                        for m in mods_sorted[:max_modules]),
        "Key classes: " + ", ".join(f"{c.name} [{c.module_path}]"
                                    for c in classes_sorted[:max_classes]),
    ]
    deps = next((m.external_deps for m in parse_result.modules if m.external_deps), [])
    if deps:
        lines.append("Declared dependencies (code in these is NOT in the repo): "
                     + ", ".join(deps[:12]))
    return "\n".join(lines)
