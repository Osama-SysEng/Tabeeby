"""Static safety policy for Python snippets supplied as data.

This module does not execute code. It rejects dangerous syntax and imports.
For untrusted code, prefer not executing it at all; if execution is required,
use a separate sandbox with a non-root user, no network, read-only filesystem,
resource limits, and a disposable worker.
"""
from __future__ import annotations

import ast
from dataclasses import dataclass


@dataclass(frozen=True)
class PythonFinding:
    rule: str
    detail: str
    line: int


BLOCKED_IMPORTS = frozenset({
    "os", "subprocess", "socket", "ctypes", "multiprocessing", "resource",
    "importlib", "pickle", "marshal", "pty", "shutil", "pathlib",
    "httpx", "requests", "urllib", "ftplib", "telnetlib",
})
BLOCKED_CALLS = frozenset({"eval", "exec", "compile", "__import__", "breakpoint", "open"})
BLOCKED_ATTRIBUTES = frozenset({"system", "popen", "spawn", "run", "Popen", "connect", "loads"})


def inspect_python_source(source: str, *, max_bytes: int = 32_000) -> list[PythonFinding]:
    if not isinstance(source, str):
        raise TypeError("source must be text")
    if len(source.encode("utf-8")) > max_bytes:
        return [PythonFinding("size_limit", "Python source exceeds the configured size limit", 1)]
    try:
        tree = ast.parse(source, mode="exec")
    except SyntaxError as exc:
        return [PythonFinding("syntax", exc.msg, exc.lineno or 1)]

    findings: list[PythonFinding] = []
    for node in ast.walk(tree):
        line = getattr(node, "lineno", 1)
        if isinstance(node, (ast.Import, ast.ImportFrom)):
            names = [alias.name.split(".")[0] for alias in node.names]
            for name in names:
                if name in BLOCKED_IMPORTS:
                    findings.append(PythonFinding("blocked_import", name, line))
        elif isinstance(node, ast.Call):
            if isinstance(node.func, ast.Name) and node.func.id in BLOCKED_CALLS:
                findings.append(PythonFinding("blocked_call", node.func.id, line))
            if isinstance(node.func, ast.Attribute) and node.func.attr in BLOCKED_ATTRIBUTES:
                findings.append(PythonFinding("blocked_attribute", node.func.attr, line))
        elif isinstance(node, ast.Attribute) and node.attr in {"__globals__", "__builtins__", "__subclasses__", "__class__"}:
            findings.append(PythonFinding("blocked_introspection", node.attr, line))
    return findings


def assert_safe_python_source(source: str, *, max_bytes: int = 32_000) -> None:
    findings = inspect_python_source(source, max_bytes=max_bytes)
    if findings:
        summary = "; ".join(f"{f.rule}:{f.detail}@{f.line}" for f in findings[:5])
        raise ValueError(f"Python source rejected by safety policy: {summary}")
