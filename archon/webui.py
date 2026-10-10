"""Local browser UI for launching and monitoring Code-Archon investigations.

The web layer only validates launch options and invokes the existing CLI. It does not
reimplement or alter repository analysis, retrieval, graph construction, or agent logic.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
import threading
import time
import webbrowser
import uuid
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse

_UI_DIR = Path(__file__).parent / "ui"
_RUNS: dict[str, dict] = {}
_LOCK = threading.RLock()
_MAX_LOG_LINES = 4000
_PHASES = [
    ("Parsing repository", "Repository scan"),
    ("Graph store", "Building code graph"),
    ("Edges:", "Mapping relationships"),
    ("Index:", "Indexing code context"),
    ("Goal decomposed", "Planning investigation"),
    ("Running agent loop", "Investigating"),
    ("Complete after", "Generating deliverables"),
    ("Dashboard →", "Finalizing dashboard"),
    ("Documentation written", "Complete"),
]


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _phase_for(line: str, current: str) -> str:
    for marker, label in _PHASES:
        if marker.lower() in line.lower():
            return label
    return current


def _read_process(run_id: str, process: subprocess.Popen[str]) -> None:
    run = _RUNS[run_id]
    try:
        assert process.stdout is not None
        for raw in process.stdout:
            line = raw.rstrip("\r\n")
            with _LOCK:
                run["logs"].append(line)
                if len(run["logs"]) > _MAX_LOG_LINES:
                    del run["logs"][:-_MAX_LOG_LINES]
                run["phase"] = _phase_for(line, run["phase"])
                run["updated_at"] = _now()
        code = process.wait()
        with _LOCK:
            run["return_code"] = code
            run["status"] = "completed" if code == 0 else "failed"
            run["phase"] = "Complete" if code == 0 else "Exited with an error"
            run["finished_at"] = _now()
            run["finished_epoch"] = time.time()
            index = run["output_path"] / "index.html"
            run["dashboard_exists"] = index.is_file()
            run["dashboard_path"] = str(index) if index.is_file() else ""
            run["updated_at"] = _now()
    except Exception as exc:
        with _LOCK:
            run["status"] = "failed"
            run["phase"] = "UI monitor error"
            run["logs"].append(f"[Code-Archon UI] Monitor error: {exc}")
            run["finished_at"] = _now()
            run["finished_epoch"] = time.time()


def _public_run(run: dict, include_logs: bool = True) -> dict:
    with _LOCK:
        result = {k: v for k, v in run.items() if k not in {"process", "logs", "output_path", "event_path", "command"}}
        result["output_path"] = str(run["output_path"])
        result["logs"] = run["logs"][-500:] if include_logs else []
        if run.get("started_epoch"):
            result["elapsed_seconds"] = round((run.get("finished_epoch") or time.time()) - run["started_epoch"])
        return result


class Handler(BaseHTTPRequestHandler):
    server_version = "CodeArchonUI/1.0"

    def log_message(self, fmt: str, *args) -> None:
        print("[Code-Archon UI] " + fmt % args)

    def _send(self, status: int, payload, content_type: str = "application/json; charset=utf-8") -> None:
        if content_type.startswith("application/json"):
            body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        elif isinstance(payload, str):
            body = payload.encode("utf-8")
        else:
            body = payload
        try:
            self.send_response(status)
            self.send_header("Content-Type", content_type)
            self.send_header("Content-Length", str(len(body)))
            self.send_header("Cache-Control", "no-store")
            self.send_header("X-Content-Type-Options", "nosniff")
            self.end_headers()
            self.wfile.write(body)
        except (BrokenPipeError, ConnectionResetError, ConnectionAbortedError):
            # The client disconnected before the response finished.
            return
    def _body(self) -> dict:
        length = int(self.headers.get("Content-Length", "0"))
        if length <= 0 or length > 64_000:
            raise ValueError("Request body is missing or too large.")
        data = json.loads(self.rfile.read(length).decode("utf-8"))
        if not isinstance(data, dict):
            raise ValueError("Expected a JSON object.")
        return data

    def do_GET(self) -> None:
        path = urlparse(self.path).path
        if path == "/" or path == "/app":
            try:
                page = (_UI_DIR / "product.html").read_text(encoding="utf-8")
            except OSError:
                self._send(500, "Customer UI file is missing.", "text/plain; charset=utf-8")
                return
            self._send(200, page, "text/html; charset=utf-8")
            return
        if path == "/dev":
            try:
                page = (_UI_DIR / "launcher.html").read_text(encoding="utf-8")
            except OSError:
                self._send(500, "Developer launcher UI file is missing.", "text/plain; charset=utf-8")
                return
            self._send(200, page, "text/html; charset=utf-8")
            return
        if path == "/live":
            try:
                page = (Path(__file__).parent / "observability" / "dashboard.html").read_text(encoding="utf-8")
            except OSError:
                self._send(500, "Observability dashboard file is missing.", "text/plain; charset=utf-8")
                return
            self._send(200, page, "text/html; charset=utf-8")
            return
        if path == "/api/infrastructure":
            try:
                from archon.observability.infrastructure import infrastructure_snapshot
                self._send(200, infrastructure_snapshot())
            except Exception as exc:
                self._send(500, {"error": f"Infrastructure probe failed: {exc}"})
            return
        if path == "/api/infrastructure/container-logs":
            query = parse_qs(urlparse(self.path).query)
            name = (query.get("name") or [""])[0]
            try:
                from archon.observability.infrastructure import container_logs
                result = container_logs(name)
                self._send(200 if not result.get("error") else 404, result)
            except Exception as exc:
                self._send(500, {"error": f"Container log inspection failed: {exc}"})
            return
        events_match = re.fullmatch(r"/api/observability/([a-f0-9-]+)/events", path)
        if events_match:
            run_id = events_match.group(1)
            with _LOCK:
                run = _RUNS.get(run_id)
                if not run:
                    self._send(404, {"error": "Run not found."})
                    return
                event_path = run.get("event_path")
            if not event_path:
                self._send(200, {"events": [], "message": "No trace path is registered for this run."})
                return
            try:
                from archon.observability.events import read_events
                self._send(200, {"events": read_events(event_path)})
            except Exception as exc:
                self._send(500, {"error": f"Could not read event trace: {exc}"})
            return
        if path == "/api/open":
            query = parse_qs(urlparse(self.path).query)
            run_id = (query.get("run") or [""])[0]
            file_kind = (query.get("file") or [""])[0]
            with _LOCK:
                run = _RUNS.get(run_id)
                if not run or run["status"] != "completed":
                    self._send(404, {"error": "Completed run not found."})
                    return
                filename = "index.html" if file_kind == "dashboard" else "report.md" if file_kind == "report" else ""
                if not filename:
                    self._send(400, {"error": "Unsupported result file."})
                    return
                target = run["output_path"] / filename
            if not target.is_file():
                self._send(404, {"error": f"{filename} was not generated."})
                return
            content_type = "text/html; charset=utf-8" if filename.endswith(".html") else "text/markdown; charset=utf-8"
            try:
                self._send(200, target.read_text(encoding="utf-8", errors="replace"), content_type)
            except OSError as exc:
                self._send(500, {"error": f"Could not read result: {exc}"})
            return
        if path == "/api/health":
            self._send(200, {"ok": True, "service": "Code-Archon UI"})
            return
        if path == "/api/runs":
            with _LOCK:
                runs = sorted(_RUNS.values(), key=lambda r: r["started_epoch"], reverse=True)
                self._send(200, {"runs": [_public_run(r, include_logs=False) for r in runs[:20]]})
            return
        match = re.fullmatch(r"/api/runs/([a-f0-9-]+)", path)
        if match:
            with _LOCK:
                run = _RUNS.get(match.group(1))
                if not run:
                    self._send(404, {"error": "Run not found."})
                    return
                self._send(200, _public_run(run))
            return
        self._send(404, {"error": "Not found."})

    def do_POST(self) -> None:
        if urlparse(self.path).path != "/api/investigations":
            self._send(404, {"error": "Not found."})
            return
        try:
            data = self._body()
            repo_raw = str(data.get("repo", "")).strip()
            goal = str(data.get("goal", "")).strip()
            output_raw = str(data.get("output", "./demo-output")).strip() or "./demo-output"
            if not repo_raw:
                raise ValueError("Choose a repository folder.")
            repo = Path(repo_raw).expanduser().resolve()
            if not repo.exists() or not repo.is_dir():
                raise ValueError("The repository path must point to an existing folder.")
            if not goal:
                raise ValueError("Enter an investigation goal.")
            if len(goal) > 2000:
                raise ValueError("Goal must be 2,000 characters or fewer.")
            try:
                max_iter = int(data.get("max_iter", 15))
            except (TypeError, ValueError):
                raise ValueError("Iteration limit must be a number.") from None
            if not 1 <= max_iter <= 50:
                raise ValueError("Iteration limit must be between 1 and 50.")
            output_path = Path(output_raw).expanduser()
            if not output_path.is_absolute():
                output_path = Path.cwd() / output_path
            output_path = output_path.resolve()
            if output_path == repo or repo in output_path.parents:
                raise ValueError("Output folder cannot be the repository folder or a folder inside it.")
            use_llm = bool(data.get("use_llm", True))
            with _LOCK:
                if any(r["status"] == "running" for r in _RUNS.values()):
                    self._send(409, {"error": "An investigation is already running. Wait for it to finish before starting another."})
                    return
                run_id = str(uuid.uuid4())
                command = [
                    sys.executable, "-m", "archon.cli", "investigate", str(repo),
                    "--goal", goal, "--output", str(output_path), "--max-iter", str(max_iter),
                    "--llm" if use_llm else "--no-llm",
                ]
                event_path = output_path / ".archon-observability" / f"{run_id}.jsonl"
                child_env = os.environ.copy()
                child_env["ARCHON_EVENT_LOG"] = str(event_path)
                proc = subprocess.Popen(
                    command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                    text=True, encoding="utf-8", errors="replace", bufsize=1,
                    cwd=str(Path.cwd()), env=child_env,
                )
                run = {
                    "id": run_id, "status": "running", "phase": "Starting investigation",
                    "repo": str(repo), "goal": goal, "output_path": output_path,
                    "event_path": event_path,
                    "use_llm": use_llm, "max_iter": max_iter,
                    "started_at": _now(), "updated_at": _now(), "finished_at": None,
                    "started_epoch": time.time(), "finished_epoch": None,
                    "return_code": None, "dashboard_exists": False, "dashboard_path": "",
                    "logs": [f"Starting Code-Archon for {repo}", "The existing investigation CLI is running unchanged."],
                    "process": proc,
                }
                _RUNS[run_id] = run
                threading.Thread(target=_read_process, args=(run_id, proc), daemon=True).start()
            self._send(202, _public_run(run))
        except (ValueError, json.JSONDecodeError) as exc:
            self._send(400, {"error": str(exc)})
        except OSError as exc:
            self._send(500, {"error": f"Could not launch investigation: {exc}"})

    def do_HEAD(self) -> None:
        if urlparse(self.path).path == "/":
            self.send_response(200)
            self.end_headers()
        else:
            self.send_response(404)
            self.end_headers()


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the Code-Archon investigation launcher UI.")
    parser.add_argument("--host", default="127.0.0.1", help="Bind address (default: 127.0.0.1)")
    parser.add_argument("--port", type=int, default=8765, help="HTTP port (default: 8765)")
    parser.add_argument("--no-browser", action="store_true", help="Do not open a browser automatically")
    args = parser.parse_args()
    if args.host not in {"127.0.0.1", "localhost", "::1"}:
        print("Warning: the UI can launch investigations on the host machine. Do not expose it to an untrusted network.", file=sys.stderr)
    server = ThreadingHTTPServer((args.host, args.port), Handler)
    url = f"http://{args.host if args.host != '::1' else '[::1]'}:{args.port}"
    print(f"Code-Archon UI running at {url}")
    print("Press Ctrl+C to stop the UI server.")
    if not args.no_browser:
        threading.Timer(0.5, lambda: webbrowser.open(url)).start()
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopping Code-Archon UI...")
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
