# Code-Archon: Fixes and Recommended Follow-up Changes

This document records the recent Windows/WebUI fixes and the broader code-review recommendations for the `feature/live-observability-ui` branch. It is a tracking document, not a claim that every recommendation below has already been implemented.

## 1. Implemented in commit `ab600e9`

Commit: [Fix Windows CLI encoding and HTTP disconnect handling](https://github.com/Madhav-Ahuja27/Code-Archon/commit/ab600e9062b2cb6678c2997ccb9df7fa72858460)

### Windows CLI encoding

**Problem:** Rich CLI output containing Unicode symbols (for example, a check mark) could raise `UnicodeEncodeError` when stdout/stderr used a legacy Windows code page.

**Change:** Reconfigure stdout and stderr to UTF-8 with replacement handling when the stream supports `reconfigure()`, before Rich's console is initialized.

**Expected result:** CLI output should not terminate solely because the active Windows console encoding cannot represent a Unicode character.

### WebUI client disconnect handling

**Problem:** A browser/client disconnect during an HTTP response could raise `BrokenPipeError`, `ConnectionResetError`, or `ConnectionAbortedError`. In an API handler with a broad exception handler, this could be misreported as an infrastructure-probe failure, followed by an attempt to send a second response over the dead connection.

**Change:** `Handler._send()` now catches those expected disconnect exceptions while writing the response.

**Expected result:** A disconnected client should not produce a misleading infrastructure error or trigger a second response attempt.

### Regression test added

A test in `tests/test_webui.py` simulates a disconnected client by making the response writer raise `ConnectionAbortedError`. It checks that `_send()` handles that expected condition without propagating it.

### Verification status

The commit and changed files were checked on GitHub. The test suite and Windows reproduction were **not run as part of that commit**, so runtime verification remains outstanding.

---

## 2. Recommended follow-up work

The items below are recommendations from the broader code review. They are **not included in commit `ab600e9` unless explicitly listed in Section 1**.

### Priority 1 — Prevent destructive or cross-investigation graph operations

**Concern:** The default CLI path may clear the Neo4j graph unless `--keep-graph` is provided. Clearing a shared graph can remove data belonging to another investigation or run.

**Recommended changes:**
- Make graph cleanup explicitly scoped to the current investigation/run, using a stable run or investigation identifier.
- Avoid global `store.clear()` operations against shared stores unless the user explicitly requests a full reset.
- Make destructive behavior explicit in CLI help and documentation; consider requiring an explicit flag for global clearing.
- Ensure vector-store cleanup does not accidentally delete embedding data needed by other investigations.

**Acceptance checks:**
- A run only removes its own graph/vector records.
- A second investigation's records remain after the first investigation is cleared.
- Any intentionally global reset is explicit and covered by a test.

### Priority 1 — Strengthen evidence verification

**Concern:** Evidence verification should reliably distinguish supported findings from claims that are merely plausible or weakly related to retrieved material.

**Recommended changes:**
- Verify that each material claim is directly supported by its cited evidence, not just by the presence of a citation.
- Track unsupported, contradictory, and insufficient-evidence outcomes separately.
- Preserve source references through retrieval, synthesis, and final verification.
- Add tests for fabricated citations, irrelevant evidence, conflicting sources, and claims only partially supported by evidence.

**Acceptance checks:**
- Unsupported claims are flagged or rejected according to the project's verification policy.
- Contradictory evidence is surfaced rather than silently ignored.
- Tests cover both valid evidence and common failure cases.

### Priority 1 — Validate Cypher identifiers and query construction

**Concern:** Dynamic labels, relationship types, property identifiers, or other query fragments can be unsafe if interpolated without validation. Parameterized query values do not parameterize Cypher identifiers.

**Recommended changes:**
- Validate dynamic identifiers against an allowlist or a strict identifier validator before query construction.
- Continue using query parameters for data values wherever supported.
- Centralize dynamic Cypher construction so validation is not inconsistently applied across call sites.

**Acceptance checks:**
- Invalid or unexpected identifiers are rejected before query execution.
- User-controlled values cannot alter query structure.
- Tests cover malformed identifiers and normal valid identifiers.

### Priority 2 — Make LLM provider fallback predictable

**Concern:** Provider fallback can behave unexpectedly if configuration errors, missing credentials, rate limits, and transient provider failures are treated identically.

**Recommended changes:**
- Define which error categories should trigger fallback and which should fail fast.
- Validate provider configuration and required credentials at startup or before the first request.
- Log the selected provider and fallback reason without logging secrets or sensitive prompt contents.
- Preserve the original failure details when all configured providers fail.

**Acceptance checks:**
- Missing credentials and invalid configuration produce actionable errors.
- Eligible transient failures trigger the configured fallback.
- Exhausting all providers returns a clear, diagnosable error.

### Priority 2 — Make test and coverage results trustworthy

**Concern:** Stale pytest/coverage report paths or ignored exit codes can make failed tests appear successful or can cause old reports to be mistaken for current results.

**Recommended changes:**
- Ensure automation propagates pytest's exit code.
- Write reports to deterministic locations and clear or replace stale outputs before a run.
- Associate generated reports with the current run where practical.
- Document the canonical local test command and expected artifacts.

**Acceptance checks:**
- A deliberately failing test makes the command or CI job fail.
- Missing or stale reports cannot be interpreted as a successful current run.
- Report paths are consistent across local and CI workflows.

### Priority 2 — Declare optional integration dependencies clearly

**Concern:** Optional LLM/provider integrations can fail at runtime when their SDKs are not installed or are not declared in the appropriate dependency group.

**Recommended changes:**
- Inventory optional integrations (including Anthropic and OpenAI clients where used).
- Declare each SDK in the appropriate optional dependency group or documented installation extra.
- Check dependencies at the integration boundary and return an actionable message when an optional SDK is missing.
- Avoid making unrelated installations heavier than necessary.

**Acceptance checks:**
- A clean environment can install the documented extras and run the selected integration.
- Missing optional SDKs produce a clear setup error rather than an opaque import failure.
- Core functionality remains usable without unused optional integrations.

### Priority 3 — Keep generated artifacts out of source control

**Concern:** Test reports, coverage files, caches, temporary investigation outputs, and other generated artifacts can clutter commits and create misleading diffs.

**Recommended changes:**
- Review repository status and existing tracked artifacts.
- Add appropriate generated paths to `.gitignore` (for example, applicable pytest/coverage outputs and Python caches).
- Remove already-tracked generated files from version control only after confirming they are reproducible and not intentionally maintained project assets.

**Acceptance checks:**
- A normal test/development run does not produce unrelated generated-file changes in `git status`.
- Required fixtures, documentation, and intentional sample outputs remain tracked.

---

## 3. Additional verification for the recent WebUI fix

The following checks are still recommended after pulling the commit:

- Run the focused WebUI tests, then the full test suite.
- Reproduce the CLI Unicode output on Windows with a legacy console code page.
- Open and close/reload the WebUI while requests are in flight; confirm disconnects do not create misleading infrastructure-probe failures.
- Exercise a genuine infrastructure-probe exception and confirm the API returns the intended error response when the client remains connected.
- Confirm that the subprocess launcher retains its existing UTF-8 text configuration (`text=True`, `encoding="utf-8"`, `errors="replace"`, `bufsize=1`); no subprocess encoding change was needed in the reviewed code.

## 4. Suggested implementation order

1. Scope graph and vector-store cleanup to an investigation/run.
2. Strengthen evidence-verification rules and tests.
3. Validate dynamic Cypher identifiers.
4. Clarify provider fallback and configuration errors.
5. Fix test/coverage report handling and declare optional dependencies.
6. Clean up generated artifacts and complete regression verification.

Implement these changes incrementally, with focused tests for each behavior. Avoid combining broad changes to investigation logic, parsing, retrieval, graph construction, agent behavior, or verification policy into a UI-only patch without reviewing their effects separately.
