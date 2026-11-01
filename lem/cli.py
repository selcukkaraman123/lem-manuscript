"""Command-line interface: `python -m lem <command> ...`"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from .claims import claim_drift_index, semantic_delta, surface_check
from .hashing import sha256_file, verify_chain
from .provenance import provenance
from .reexecute import reexecute
from .validate import load, validate


def _print(obj) -> None:
    print(json.dumps(obj, ensure_ascii=False, indent=2))


def _h_claims(manuscript: str) -> list[str]:
    """Reference set for CDI: the indexed claims plus every claim-like sentence of the H layer."""
    from .claims import split_claims
    _, _, claims, h_text = load(manuscript)
    return [c["text"] for c in claims] + split_claims(h_text)


def main(argv=None) -> int:
    p = argparse.ArgumentParser(prog="lem", description="Layered Executable Manuscript toolkit (v0.1)")
    sub = p.add_subparsers(dest="cmd", required=True)

    s = sub.add_parser("validate", help="schema, hash chain, H integrity, anchors, conformance level")
    s.add_argument("manuscript")

    s = sub.add_parser("verify-chain", help="check the P-layer hash chain only")
    s.add_argument("manuscript")

    s = sub.add_parser("reexecute", help="re-run analytic P-steps and compare with sealed outputs")
    s.add_argument("manuscript")
    s.add_argument("--backend", default="mock", help="'mock' (default, offline) or 'ollama:<model>'")

    s = sub.add_parser("cdi", help="Claim Drift Index of a reader rendering against the H layer")
    s.add_argument("manuscript")
    s.add_argument("rendering", help="path to a text file (an AI summary, translation, etc.)")
    s.add_argument("--threshold", type=float, default=0.30)

    s = sub.add_parser("delta", help="claim-level semantic delta between two texts")
    s.add_argument("before")
    s.add_argument("after")

    s = sub.add_parser("surface-check", help="should a 'surface' edit be escalated to substantive?")
    s.add_argument("before", help="text before the edit (string or path)")
    s.add_argument("after", help="text after the edit (string or path)")

    s = sub.add_parser("provenance", help="division-of-labor report from the claim index and override logs")
    s.add_argument("manuscript")

    s = sub.add_parser("seal", help="recompute manifest.h_hash after the author edits the H layer")
    s.add_argument("manuscript")

    a = p.parse_args(argv)

    def read(x: str) -> str:
        return Path(x).read_text(encoding="utf-8") if Path(x).is_file() else x

    if a.cmd == "validate":
        r = validate(a.manuscript)
        _print(r)
        return 0 if r["valid"] else 1
    if a.cmd == "verify-chain":
        _, steps, _, _ = load(a.manuscript)
        probs = verify_chain(steps)
        _print({"n_steps": len(steps), "intact": not probs, "problems": probs})
        return 0 if not probs else 1
    if a.cmd == "reexecute":
        _print(reexecute(a.manuscript, a.backend))
        return 0
    if a.cmd == "cdi":
        r = claim_drift_index(read(a.rendering), _h_claims(a.manuscript), a.threshold)
        r.pop("matches")
        _print(r)
        return 0
    if a.cmd == "delta":
        _print(semantic_delta(read(a.before), read(a.after)))
        return 0
    if a.cmd == "surface-check":
        _print(surface_check(read(a.before), read(a.after)))
        return 0
    if a.cmd == "provenance":
        _print(provenance(a.manuscript))
        return 0
    if a.cmd == "seal":
        root = Path(a.manuscript)
        m = json.loads((root / "manifest.json").read_text(encoding="utf-8"))
        m["h_hash"] = sha256_file(root / m["h_layer"])
        (root / "manifest.json").write_text(json.dumps(m, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        _print({"h_hash": m["h_hash"]})
        return 0
    return 2


if __name__ == "__main__":
    sys.exit(main())
