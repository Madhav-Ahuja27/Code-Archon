"""Best-effort, read-only infrastructure probes for the observability UI."""
from __future__ import annotations

import json
import os
import shutil
import socket
import subprocess
import time
from typing import Any


def _tcp(host: str, port: int, timeout: float = 0.45) -> tuple[bool, float | None, str]:
    started = time.perf_counter()
    try:
        with socket.create_connection((host, port), timeout=timeout):
            return True, round((time.perf_counter() - started) * 1000, 1), "TCP connection succeeded"
    except OSError as exc:
        return False, None, str(exc)


def _docker_snapshot() -> dict[str, Any]:
    if not shutil.which("docker"):
        return {"status": "unavailable", "message": "Docker CLI is not installed or not on PATH", "containers": []}
    try:
        proc = subprocess.run(
            ["docker", "ps", "-a", "--format", "{{json .}}"],
            capture_output=True, text=True, timeout=2.5, check=False,
        )
        if proc.returncode:
            return {"status": "unavailable", "message": (proc.stderr or "Docker command failed").strip()[:500], "containers": []}
        containers = []
        for line in proc.stdout.splitlines():
            try:
                raw = json.loads(line)
            except json.JSONDecodeError:
                continue
            name = str(raw.get("Names", ""))
            if any(term in name.lower() for term in ("neo4j", "redis", "archon")):
                containers.append({
                    "name": name,
                    "image": raw.get("Image", ""),
                    "state": raw.get("State", "unknown"),
                    "status": raw.get("Status", ""),
                    "ports": raw.get("Ports", ""),
                })
        return {"status": "connected", "message": f"Docker responded; {len(containers)} relevant container(s) found", "containers": containers}
    except (OSError, subprocess.TimeoutExpired) as exc:
        return {"status": "unavailable", "message": str(exc)[:500], "containers": []}


def _redis_probe(host: str, port: int) -> dict[str, Any]:
    ok, latency, message = _tcp(host, port)
    result: dict[str, Any] = {"name": "Redis", "status": "reachable" if ok else "unavailable", "endpoint": f"{host}:{port}", "latency_ms": latency, "message": message}
    try:
        import redis
        client = redis.Redis(host=host, port=port, socket_connect_timeout=0.6, socket_timeout=0.6, decode_responses=True)
        started = time.perf_counter()
        client.ping()
        result.update(status="healthy", latency_ms=round((time.perf_counter() - started) * 1000, 1), message="PING succeeded")
        try:
            result["connected_clients"] = int(client.info("clients").get("connected_clients", 0))
            result["used_memory_human"] = client.info("memory").get("used_memory_human", "unknown")
        except Exception:
            pass
        client.close()
    except ImportError:
        if ok:
            result["message"] = "TCP reachable; install redis-py to inspect PING and metrics"
    except Exception as exc:
        result.update(status="reachable" if ok else "unavailable", message=str(exc)[:500])
    return result


def _neo4j_probe(uri: str, user: str, password: str) -> dict[str, Any]:
    host = "localhost"
    port = 7687
    try:
        from urllib.parse import urlparse
        parsed = urlparse(uri)
        host = parsed.hostname or host
        port = parsed.port or port
    except Exception:
        pass
    ok, latency, message = _tcp(host, port)
    result: dict[str, Any] = {"name": "Neo4j", "status": "reachable" if ok else "unavailable", "endpoint": f"{host}:{port}", "latency_ms": latency, "message": message}
    try:
        from neo4j import GraphDatabase
        started = time.perf_counter()
        driver = GraphDatabase.driver(uri, auth=(user, password), connection_timeout=1.0)
        try:
            driver.verify_connectivity()
            result.update(status="healthy", latency_ms=round((time.perf_counter() - started) * 1000, 1), message="Bolt connectivity and authentication succeeded")
            with driver.session() as session:
                record = session.run("MATCH (n) RETURN count(n) AS nodes").single()
                result["node_count"] = int(record["nodes"]) if record else 0
        finally:
            driver.close()
    except ImportError:
        if ok:
            result["message"] = "Bolt port reachable; install neo4j driver to verify authentication"
    except Exception as exc:
        result.update(status="reachable" if ok else "unavailable", message=str(exc)[:500])
    return result


def infrastructure_snapshot() -> dict[str, Any]:
    """Probe current local dependencies; each result describes observed state only."""
    redis_url = os.environ.get("REDIS_URL", "redis://localhost:6379")
    try:
        from urllib.parse import urlparse
        parsed = urlparse(redis_url)
        redis_host, redis_port = parsed.hostname or "localhost", parsed.port or 6379
    except Exception:
        redis_host, redis_port = "localhost", 6379
    try:
        from archon.config import cfg
        neo_uri, neo_user, neo_password = cfg.neo4j_uri, cfg.neo4j_user, cfg.neo4j_password
    except Exception:
        neo_uri, neo_user, neo_password = "bolt://localhost:7687", "neo4j", os.environ.get("NEO4J_PASSWORD", "archon-dev")
    return {
        "timestamp": time.time(),
        "docker": _docker_snapshot(),
        "services": [
            _neo4j_probe(neo_uri, neo_user, neo_password),
            _redis_probe(redis_host, redis_port),
        ],
        "note": "Read-only point-in-time probes. A reachable port does not guarantee that the application is using that service.",
    }
