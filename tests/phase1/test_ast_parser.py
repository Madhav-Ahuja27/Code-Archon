"""Phase 1 — Static Ingestion + AST Parser tests.

Gate: all 9 pass before Phase 2 begins.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from archon.ingestion.ast_parser import (
    ClassNode,
    FunctionNode,
    ModuleNode,
    ParseResult,
    parse_file,
    parse_repository,
    read_external_deps,
)

FIXTURES = Path(__file__).parent.parent.parent / "fixtures" / "sample_repo"


# ── Test 1: single file → correct ModuleNode ────────────────────────────────

def test_parses_single_file():
    auth_py = FIXTURES / "auth.py"
    module, classes, functions, error = parse_file(auth_py, FIXTURES)

    assert error is None
    assert isinstance(module, ModuleNode)
    assert module.id == "auth.py"
    assert "auth" in module.path
    assert module.docstring == "Authentication module for the sample app."
    assert module.line_count > 0


# ── Test 2: class with methods → ClassNode + FunctionNodes ──────────────────

def test_extracts_classes():
    auth_py = FIXTURES / "auth.py"
    _, classes, functions, _ = parse_file(auth_py, FIXTURES)

    class_names = [c.name for c in classes]
    assert "UserAuth" in class_names

    ua = next(c for c in classes if c.name == "UserAuth")
    assert ua.docstring == "Handles user authentication."
    assert "hash_password" in ua.methods
    assert "verify_password" in ua.methods
    # functions include the methods
    fn_names = [f.name for f in functions]
    assert "hash_password" in fn_names
    assert "verify_password" in fn_names


# ── Test 3: function calls detected ─────────────────────────────────────────

def test_extracts_function_calls():
    api_py = FIXTURES / "api.py"
    _, _, functions, _ = parse_file(api_py, FIXTURES)

    login_fn = next((f for f in functions if f.name == "login"), None)
    assert login_fn is not None, "login() not found"
    # login calls create_auth, hash_password, verify_password
    assert "create_auth" in login_fn.calls
    assert "hash_password" in login_fn.calls
    assert "verify_password" in login_fn.calls


# ── Test 4: no docstring → None, no crash ───────────────────────────────────

def test_handles_no_docstring():
    utils_py = FIXTURES / "utils.py"
    module, _, functions, error = parse_file(utils_py, FIXTURES)

    assert error is None
    assert module is not None
    assert module.docstring is None  # utils.py has no module docstring

    load_fn = next((f for f in functions if f.name == "load_config"), None)
    assert load_fn is not None
    assert load_fn.docstring is None


# ── Test 5: syntax error → logged, skipped, no crash ────────────────────────

def test_handles_syntax_error():
    bad_py = FIXTURES / "bad.py"
    module, classes, functions, error = parse_file(bad_py, FIXTURES)

    assert module is None
    assert classes == []
    assert functions == []
    assert error is not None
    assert "SyntaxError" in error or "Cannot read" in error


# ── Test 6: directory walk → correct module count ───────────────────────────

def test_walks_directory():
    result = parse_repository(FIXTURES)

    # bad.py fails, so 4 valid py files: auth, models, api, utils
    module_ids = [m.id for m in result.modules]
    assert "auth.py" in module_ids
    assert "models.py" in module_ids
    assert "api.py" in module_ids
    assert "utils.py" in module_ids
    # complex.py added in Phase 5 for radon/semgrep testing — 5 valid modules total
    assert len(result.modules) >= 4
    # bad.py in errors
    assert any("bad.py" in e for e in result.errors)


# ── Test 7: external deps read from requirements.txt ────────────────────────

def test_extracts_external_deps():
    deps = read_external_deps(FIXTURES)
    assert "flask" in deps
    assert "sqlalchemy" in deps
    assert "requests" in deps
    assert "pydantic" in deps


# ── Test 8: complexity score > 0 for complex function ───────────────────────

def test_complexity_score():
    """radon CC score must be ≥ 1 for any function."""
    result = parse_repository(FIXTURES)
    for fn in result.functions:
        assert fn.complexity >= 1, f"{fn.id} has complexity < 1"


# ── Test 9: inheritance captured in ClassNode.bases ─────────────────────────

def test_import_resolution():
    """ClassNode.bases must capture parent class names."""
    models_py = FIXTURES / "models.py"
    _, classes, _, _ = parse_file(models_py, FIXTURES)

    class_map = {c.name: c for c in classes}
    assert "User" in class_map
    assert "Base" in class_map["User"].bases

    assert "AdminUser" in class_map
    assert "User" in class_map["AdminUser"].bases
