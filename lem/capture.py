"""Capture logger (LEM-2 prototype).

A thin wrapper that sits between the researcher and the model. Every call is
written as a P-layer record, timestamped and sealed into a hash chain at the
moment it happens, so records cannot be curated after the fact.

Records written through this module carry ``capture.source = "capture-logger"``.
Records assembled by authors afterwards carry ``"author-assembled"`` and can
reach LEM-1 at most.
"""
from __future__ import annotations

import datetime as _dt
import json
from pathlib import Path

from .hashing import GENESIS, record_hash, sha256_text


def _now() -> str:
    return _dt.datetime.now(_dt.timezone.utc).replace(microsecond=0).isoformat()


class CaptureLog:
    """Append-only, hash-chained log stored as one JSON file per record."""

    def __init__(self, directory: str | Path, source: str = "capture-logger"):
        self.dir = Path(directory)
        self.dir.mkdir(parents=True, exist_ok=True)
        self.source = source

    def records(self) -> list[dict]:
        files = sorted(self.dir.glob("*.json"))
        return [json.loads(f.read_text(encoding="utf-8")) for f in files]

    def _head(self) -> str:
        recs = self.records()
        return recs[-1]["hash"] if recs else GENESIS

    def append(self, record: dict, timestamp: str | None = None) -> dict:
        rec = dict(record)
        rec.setdefault("timestamp", timestamp or _now())
        rec["capture"] = rec.get("capture") or {"source": self.source}
        rec["prev_hash"] = self._head()
        rec.pop("hash", None)
        rec["hash"] = record_hash(rec)
        n = len(list(self.dir.glob("*.json"))) + 1
        path = self.dir / f"{n:03d}_{rec['id']}.json"
        path.write_text(json.dumps(rec, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        return rec


def captured_call(log: CaptureLog, backend, step_id: str, prompt: str, text: str,
                  input_ref: str = "", temperature: float = 0.0, seed: int = 0) -> dict:
    """Call the model and seal the call as a P_analytic record in one step."""
    output = backend.generate(prompt, text, temperature=temperature, seed=seed)
    record = {
        "id": step_id,
        "type": "P_analytic",
        "model": {
            "name": backend.name,
            "version": backend.version,
            "provider": backend.provider,
            "open_weights": backend.open_weights,
        },
        "prompt": prompt,
        "parameters": {"temperature": temperature, "seed": seed},
        "input_ref": input_ref,
        "input_hash": sha256_text(text),
        "output": output,
        "output_hash": sha256_text(output),
    }
    return log.append(record)
