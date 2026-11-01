"""Canonical hashing for LEM records.

Every P-layer record is hashed over its canonical JSON form (sorted keys, no
whitespace) with the ``hash`` field removed. Each record also carries the hash
of the previous record (``prev_hash``), so the P layer forms a hash chain: any
later edit, deletion or reordering of a record breaks every hash after it.
"""
from __future__ import annotations

import hashlib
import json
from typing import Any

GENESIS = "GENESIS"


def canonical(obj: Any) -> str:
    return json.dumps(obj, sort_keys=True, ensure_ascii=False, separators=(",", ":"))


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def sha256_file(path) -> str:
    with open(path, "rb") as fh:
        return hashlib.sha256(fh.read()).hexdigest()


def record_hash(record: dict) -> str:
    body = {k: v for k, v in record.items() if k != "hash"}
    return sha256_text(canonical(body))


def verify_chain(records: list[dict]) -> list[str]:
    """Return a list of problems; an empty list means the chain is intact."""
    problems: list[str] = []
    prev = GENESIS
    for i, rec in enumerate(records):
        rid = rec.get("id", f"#{i}")
        if rec.get("prev_hash") != prev:
            problems.append(f"{rid}: prev_hash does not match the previous record (chain broken or reordered)")
        expected = record_hash(rec)
        if rec.get("hash") != expected:
            problems.append(f"{rid}: hash mismatch (record was modified after sealing)")
        prev = rec.get("hash", "")
    return problems
