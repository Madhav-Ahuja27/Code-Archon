"""AST-based static ingestion for Python repositories.

Produces ModuleNode, ClassNode, FunctionNode Pydantic models
from any Python source tree. Handles syntax errors gracefully.
"""

from __future__ import annotations

import ast
import logging
from pathlib import Path
from typing import Optional

from pydantic import BaseModel, Field

try:
    from radon.complexity import cc_visit
    from radon.metrics import mi_visit
    _RADON = True
except ImportError:
    _RADON = False

log = logging.getLogger(__name__)


# ── Data models ───────────────────────────────────────────────────────────────

class FunctionNode(BaseModel):
    id: str                          # "module_path::ClassName::fn_name"
    name: str
    module_path: str                 # relative path from repo root
    class_name: Optional[str] = None
    args: list[str] = Field(default_factory=list)
    return_type: Optional[str] = None
    docstring: Optional[str] = None
    calls: list[str] = Field(default_factory=list)  # names of fns called
    line_start: int = 0
    line_end: int = 0
    complexity: int = 1              # radon CC score


class ClassNode(BaseModel):
    id: str                          # "module_path::ClassName"
    name: str
    module_path: str
    bases: list[str] = Field(default_factory=list)
    docstring: Optional[str] = None
    methods: list[str] = Field(default_factory=list)
    line_start: int = 0
    line_end: int = 0


class ModuleNode(BaseModel):
    id: str                          # relative path
    path: str                        # absolute path
    docstring: Optional[str] = None
    imports: list[str] = Field(default_factory=list)     # all imported names
    external_deps: list[str] = Field(default_factory=list)  # from requirements
    line_count: int = 0
    avg_complexity: float = 0.0


class ParseResult(BaseModel):
    modules: list[ModuleNode] = Field(default_factory=list)
    classes: list[ClassNode] = Field(default_factory=list)
    functions: list[FunctionNode] = Field(default_factory=list)
    errors: list[str] = Field(default_factory=list)


# ── Helpers ───────────────────────────────────────────────────────────────────

def _get_docstring(node: ast.AST) -> Optional[str]:
    return ast.get_docstring(node)


def _get_annotation(node: Optional[ast.expr]) -> Optional[str]:
    if node is None:
        return None
    try:
        return ast.unparse(node)
    except Exception:
        return None


def _extract_calls(func_node: ast.FunctionDef | ast.AsyncFunctionDef) -> list[str]:
    """Walk function body, collect all Call node function names."""
    calls = []
    for child in ast.walk(func_node):
        if isinstance(child, ast.Call):
            if isinstance(child.func, ast.Name):
                calls.append(child.func.id)
            elif isinstance(child.func, ast.Attribute):
                calls.append(child.func.attr)
    return list(dict.fromkeys(calls))  # deduplicate, preserve order


def _extract_imports(tree: ast.Module) -> list[str]:
    imports = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                imports.append(alias.name)
        elif isinstance(node, ast.ImportFrom):
            module = node.module or ""
            for alias in node.names:
                imports.append(f"{module}.{alias.name}" if module else alias.name)
    return imports


def _radon_complexity(source: str) -> dict[str, int]:
    """Returns {fn_name: cc_score}. Returns {} if radon not available."""
    if not _RADON:
        return {}
    try:
        results = cc_visit(source)
        return {r.name: r.complexity for r in results}
    except Exception:
        return {}


def _avg_complexity(cc_map: dict[str, int]) -> float:
    if not cc_map:
        return 0.0
    return sum(cc_map.values()) / len(cc_map)


# ── Core parser ───────────────────────────────────────────────────────────────

def parse_file(file_path: Path, repo_root: Path) -> tuple[
    Optional[ModuleNode],
    list[ClassNode],
    list[FunctionNode],
    Optional[str],        # error string or None
]:
    """Parse a single .py file. Returns (module, classes, functions, error)."""
    try:
        raw = file_path.read_bytes()
        source = raw.decode("utf-8", errors="replace")
    except OSError as e:
        return None, [], [], f"Cannot read {file_path}: {e}"

    try:
        tree = ast.parse(raw, filename=str(file_path))
    except SyntaxError as e:
        log.warning("Syntax error in %s: %s", file_path, e)
        return None, [], [], f"SyntaxError in {file_path}: {e}"

    rel_path = file_path.relative_to(repo_root).as_posix()   # forward slashes on every OS
    cc_map = _radon_complexity(source)

    # Module node
    module = ModuleNode(
        id=rel_path,
        path=str(file_path),
        docstring=_get_docstring(tree),
        imports=_extract_imports(tree),
        line_count=len(source.splitlines()),
        avg_complexity=_avg_complexity(cc_map),
    )

    classes: list[ClassNode] = []
    functions: list[FunctionNode] = []
    seen_ids: set[str] = set()

    def _unique(base_id: str, lineno: int) -> str:
        """Same name can be defined many times in one file (nested defs, redefinitions).
        First one keeps the readable id; later ones get '@L<line>' appended."""
        nid = base_id if base_id not in seen_ids else f"{base_id}@L{lineno}"
        seen_ids.add(nid)
        return nid

    def _visit(node: ast.AST, scope: list[str], class_name: Optional[str]) -> None:
        for child in ast.iter_child_nodes(node):
            if isinstance(child, ast.ClassDef):
                chain = scope + [child.name]
                bases = [_get_annotation(b) or "" for b in child.bases]
                methods = [
                    n.name for n in child.body
                    if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))
                ]
                classes.append(ClassNode(
                    id=_unique(f"{rel_path}::{'::'.join(chain)}", child.lineno),
                    name=child.name,
                    module_path=rel_path,
                    bases=[b for b in bases if b],
                    docstring=_get_docstring(child),
                    methods=list(dict.fromkeys(methods)),
                    line_start=child.lineno,
                    line_end=child.end_lineno or child.lineno,
                ))
                _visit(child, chain, child.name)

            elif isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef)):
                chain = scope + [child.name]
                functions.append(FunctionNode(
                    id=_unique(f"{rel_path}::{'::'.join(chain)}", child.lineno),
                    name=child.name,
                    module_path=rel_path,
                    class_name=class_name,
                    args=[a.arg for a in child.args.args],
                    return_type=_get_annotation(child.returns),
                    docstring=_get_docstring(child),
                    calls=_extract_calls(child),
                    line_start=child.lineno,
                    line_end=child.end_lineno or child.lineno,
                    complexity=cc_map.get(child.name, 1),
                ))
                _visit(child, chain, class_name)

            else:
                _visit(child, scope, class_name)

    _visit(tree, [], None)

    return module, classes, functions, None


# ── External dependency reader ────────────────────────────────────────────────

def read_external_deps(repo_root: Path) -> list[str]:
    """Read package names from requirements.txt or pyproject.toml."""
    deps: list[str] = []

    req_file = repo_root / "requirements.txt"
    if req_file.exists():
        for line in req_file.read_text(encoding="utf-8", errors="replace").splitlines():
            line = line.strip()
            if line and not line.startswith("#"):
                # strip version specifiers
                name = line.split(">=")[0].split("==")[0].split("<=")[0].split("[")[0].strip()
                if name:
                    deps.append(name)

    pyproject = repo_root / "pyproject.toml"
    if pyproject.exists():
        try:
            import tomllib  # py 3.11+
            data = tomllib.loads(pyproject.read_text(encoding="utf-8"))
            raw = data.get("project", {}).get("dependencies", [])
            for dep in raw:
                name = dep.split(">=")[0].split("==")[0].split("<=")[0].split("[")[0].strip()
                if name:
                    deps.append(name)
        except Exception:
            pass

    return list(dict.fromkeys(deps))


# ── Directory walker ──────────────────────────────────────────────────────────

def parse_repository(repo_root: Path) -> ParseResult:
    """Walk an entire repo root and parse all .py files.

    Skips: venv/, .venv/, __pycache__/, .git/, node_modules/, build/, dist/
    """
    SKIP_DIRS = {
        "venv", ".venv", "__pycache__", ".git",
        "node_modules", "build", "dist", ".eggs", ".tox",
    }

    result = ParseResult()
    external_deps = read_external_deps(repo_root)

    py_files = [
        p for p in repo_root.rglob("*.py")
        if not any(skip in p.parts for skip in SKIP_DIRS)
    ]

    for py_file in sorted(py_files):
        module, classes, functions, error = parse_file(py_file, repo_root)
        if error:
            result.errors.append(error)
            continue
        if module:
            module.external_deps = external_deps
            result.modules.append(module)
        result.classes.extend(classes)
        result.functions.extend(functions)

    return result
