"""Provenance report: who contributed what to the H layer (the cognitive division of labor)."""
from __future__ import annotations

from collections import Counter
from pathlib import Path

from .validate import load


def provenance(manuscript_dir: str | Path) -> dict:
    manifest, steps, claims, _ = load(manuscript_dir)
    origins = Counter(c["origin"] for c in claims)
    decisions = Counter(
        e["decision"] for s in steps for e in s.get("override_log", [])
    )
    by_type = Counter(s["type"] for s in steps)
    n = len(claims) or 1
    traced_to_ideation = sum(
        1 for c in claims
        if any(sid in {s["id"] for s in steps if s["type"] == "P_ideation"} for sid in c["p_steps"])
    )
    total_dec = sum(decisions.values()) or 1
    return {
        "title": manifest["title"],
        "conformance_level": manifest["conformance_level"],
        "claims_by_origin": {k: {"n": v, "share": round(v / n, 2)} for k, v in origins.items()},
        "share_of_claims_traceable_to_P_ideation": round(traced_to_ideation / n, 2),
        "override_decisions": {k: {"n": v, "share": round(v / total_dec, 2)} for k, v in decisions.items()},
        "p_steps_by_type": dict(by_type),
    }
