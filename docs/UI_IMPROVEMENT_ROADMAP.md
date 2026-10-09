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

## Step 3 — Improve evidence navigation (in progress)

- [x] Add search and status filters to findings and unresolved items.
- [ ] Make every supported claim open its cited file and line window.
- Explain which evidence supports, contradicts, or fails to establish each claim.
- Make evidence provenance and missing provenance visually distinct.

## Step 4 — Make the systems view easier to operate (planned)

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
