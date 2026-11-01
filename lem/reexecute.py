"""Re-execute analytic P-steps and compare outputs with the sealed reference outputs."""
from __future__ import annotations

from pathlib import Path

from .backends import get_backend
from .hashing import sha256_text
from .validate import load


def reexecute(manuscript_dir: str | Path, backend_spec: str = "mock", inputs: dict | None = None) -> dict:
    root = Path(manuscript_dir)
    manifest, steps, _, _ = load(root)
    backend = get_backend(backend_spec)
    inputs = inputs or {}
    results = []
    for s in steps:
        if s["type"] != "P_analytic":
            continue
        ref = s.get("input_ref", "")
        text = inputs.get(ref)
        if text is None and ref:
            src, _, line = ref.partition("#L")
            lines = (root / src).read_text(encoding="utf-8").splitlines()
            text = lines[int(line) - 1] if line else "\n".join(lines)
        if sha256_text(text) != s["input_hash"]:
            results.append({"id": s["id"], "status": "input-changed"})
            continue
        p = s.get("parameters", {})
        out = backend.generate(s["prompt"], text, temperature=p.get("temperature", 0.0), seed=p.get("seed", 0))
        results.append({
            "id": s["id"],
            "reference": s["output"],
            "reexecuted": out,
            "exact_match": sha256_text(out) == s["output_hash"],
        })
    n = len(results)
    k = sum(1 for r in results if r.get("exact_match"))
    return {
        "manuscript": str(root),
        "backend": f"{backend.name} ({backend.provider})",
        "n_analytic_steps": n,
        "exact_match_rate": round(k / n, 3) if n else None,
        "results": results,
    }
