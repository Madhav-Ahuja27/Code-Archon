# UI improvement roadmap

This roadmap prioritizes user trust and visibility over decorative polish. Investigation algorithms and evidence-gating decisions are out of scope unless a UI defect requires a separately reviewed change.

## Step 1 — Make uncertainty visible everywhere (implemented; runtime verification pending)

- Keep unsupported tasks and hypotheses visible instead of silently dropping them.
- Use a dedicated **NOT VERIFIED** label whenever there is no verified finding.
- Preserve more specific statuses such as **UNRESOLVED** and **REJECTED**, but pair them with **NOT VERIFIED** so users cannot mistake them for established facts.
- Explain that missing verification is unknown, not proof that a claim is false.
- Add a separate not-verified panel to the generated report dashboard.

## Step 2 — Bring live operational activity into the customer flow (implemented; runtime verification pending)

- Show the actual recorded agent event stream inside the progress modal.
- Let users filter agent stages, tool calls, evidence/findings, and errors.
- Show bounded, inspectable event details without exposing hidden model chain-of-thought.
- Display Docker, Neo4j, and Redis host probes with an explicit warning that reachability alone does not prove the current run uses that service.
- Keep the full /live systems view available for deeper diagnosis.

## Step 3 — Improve evidence navigation (partially implemented; runtime verification pending)

- [x] Add search and status filters to findings and unresolved items.
- [x] Make every finding with an embedded source reference open its cited file and highlighted line window.
- [x] Explain why source lines cannot be shown when provenance is missing or no excerpt was embedded.
- [x] Make evidence references clickable and missing provenance visually distinct.
- [ ] Add explicit per-evidence support/contradiction/insufficient labels from structured evidence metadata; do not infer them from text.

## Frontend usability pass — navigation and keyboard access (implemented; runtime verification pending)

- Keep primary navigation visible and horizontally scrollable on narrow screens instead of hiding it entirely.
- Make the progress dialog keyboard-operable with Escape-to-close, focus containment, focus restoration, and background scroll locking.
- Respect reduced-motion preferences.

## Step 4 — Make the systems view easier to operate (partially implemented; runtime verification pending)

- Group events by investigation stage and collapse repetitive low-level events by default.
- Add pause/resume auto-refresh, clear stale-data indicators, and copy/export for event payloads.
- Separate *service reachable*, *service configured*, and *service observed in this run* states.
- Add accessible color-independent labels, keyboard operation, and small-screen layouts.

## Step 5 — End-to-end verification (pending)

- Run the focused UI/export tests and full test suite.
- Execute an actual investigation with available Docker, Neo4j, and Redis services.
- Confirm that events appear live, that unsupported tasks receive NOT VERIFIED labels, and that infrastructure failures do not change investigation behavior.
- Record screenshots and the exact tested configuration before calling the UI verified.

## Trust and safety rules

- Never infer **VERIFIED** from absence of an error or from a reachable service.
- Never present **NOT VERIFIED** as **FALSE**.
- Do not invent activity when the engine has not emitted an event; label it as unobserved or not instrumented.
- Keep local operational logs and source excerpts private; they may contain sensitive repository information.
- Treat host infrastructure probes as snapshots unless a run-specific connection is directly observed.
