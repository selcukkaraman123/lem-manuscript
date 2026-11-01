"""Validate a LEM manuscript: schema, hash chain, H-layer integrity, anchors and conformance level."""
from __future__ import annotations

import json
import re
from pathlib import Path

from jsonschema import Draft202012Validator

from .hashing import sha256_file, verify_chain

SCHEMA_PATH = Path(__file__).resolve().parent.parent / "schema" / "lem-v0.1.schema.json"


def _validator(defname: str) -> Draft202012Validator:
    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    sub = {"$schema": schema["$schema"], "$defs": schema["$defs"], "$ref": f"#/$defs/{defname}"}
    return Draft202012Validator(sub)


def load(manuscript_dir: str | Path) -> tuple[dict, list[dict], list[dict], str]:
    root = Path(manuscript_dir)
    manifest = json.loads((root / "manifest.json").read_text(encoding="utf-8"))
    steps = [json.loads((root / p).read_text(encoding="utf-8")) for p in manifest["p_steps"]]
    claims = json.loads((root / manifest["claims"]).read_text(encoding="utf-8"))
    h_text = (root / manifest["h_layer"]).read_text(encoding="utf-8")
    return manifest, steps, claims, h_text


def validate(manuscript_dir: str | Path) -> dict:
    root = Path(manuscript_dir)
    errors: list[str] = []
    warnings: list[str] = []
    manifest, steps, claims, h_text = load(root)

    for e in _validator("manifest").iter_errors(manifest):
        errors.append(f"manifest: {e.message}")

    step_v = _validator("step")
    for s in steps:
        for e in step_v.iter_errors(s):
            errors.append(f"{s.get('id', '?')}: schema: {e.message[:200]}")

    claim_v = _validator("claim")
    for c in claims:
        for e in claim_v.iter_errors(c):
            errors.append(f"{c.get('id', '?')}: schema: {e.message}")

    # 1. hash chain
    errors.extend(verify_chain(steps))

    # 2. H layer has not changed since the manifest was sealed
    h_hash = sha256_file(root / manifest["h_layer"])
    if h_hash != manifest.get("h_hash"):
        errors.append("H layer: file hash differs from manifest.h_hash (H changed after sealing; re-seal with `lem seal`)")

    # 3. anchors: every claim points to existing steps and appears in H
    step_ids = {s["id"] for s in steps}
    anchors_in_h = set(re.findall(r"\[(C\d+)\]", h_text))
    for c in claims:
        for sid in c["p_steps"]:
            if sid not in step_ids:
                errors.append(f"{c['id']}: refers to unknown P-step '{sid}'")
        if c["id"] not in anchors_in_h:
            errors.append(f"{c['id']}: claim anchor not found in H layer")
    for a in sorted(anchors_in_h - {c["id"] for c in claims}):
        errors.append(f"H layer: anchor [{a}] has no entry in the claim index")

    # 4. conformance level rules
    level = manifest.get("conformance_level")
    types = {s["type"] for s in steps}
    if level == "LEM-0" and types - {"P_analytic"}:
        errors.append("LEM-0 allows only P_analytic steps")
    if level in ("LEM-1", "LEM-2"):
        for s in steps:
            if s["type"] == "P_surface" and s.get("escalated"):
                warnings.append(f"{s['id']}: surface step was escalated; it must be re-logged as P_drafting with full text")
    if level == "LEM-2":
        for s in steps:
            if s["capture"]["source"] != "capture-logger":
                errors.append(f"{s['id']}: LEM-2 requires records written by the capture logger (found '{s['capture']['source']}')")

    # 5. redactions are visible, not silent
    n_redacted = sum(1 for s in steps for v in s.values() if isinstance(v, dict) and v.get("redacted"))

    return {
        "manuscript": str(root),
        "conformance_level": level,
        "n_steps": len(steps),
        "n_claims": len(claims),
        "n_redacted_fields": n_redacted,
        "valid": not errors,
        "errors": errors,
        "warnings": warnings,
    }
