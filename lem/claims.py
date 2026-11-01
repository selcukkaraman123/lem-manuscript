"""Claim matching: Claim Drift Index (CDI), semantic delta and surface escalation.

The offline engine used here is deliberately simple and transparent:

* a text is split into candidate atomic claims (sentences and list items);
* each claim is represented as a TF-IDF vector over content words;
* a claim is "supported" when its best cosine match in the reference set
  reaches a threshold.

This lexical baseline is the reference point for the LLM-judge version planned
in the proposal (atomic-fact matching in the style of FActScore, Min et al.,
2023). It cannot detect contradiction, only lack of support; contradiction
detection is listed as planned work in STATUS.md.
"""
from __future__ import annotations

import math
import re
from collections import Counter
from difflib import SequenceMatcher

STOP = set("""
a an the and or but if of to in on for with by from as at is are was were be been being this that these
those it its into than then so such not no can could may might will would should do does did has have had
which who whom whose what when where how each every any all both either neither one two three our their
we they he she you i also only more most less very per via about over under between across within without
""".split())

HEDGES_WEAK = ("may", "might", "could", "suggest", "suggests", "possibly", "likely", "appears", "indicate", "indicates", "tentative")
HEDGES_STRONG = ("demonstrate", "demonstrates", "prove", "proves", "establish", "establishes", "show conclusively", "confirm", "confirms", "always", "never")

DEFAULT_THRESHOLD = 0.30
ESCALATION_THRESHOLD = 0.15


def split_claims(text: str) -> list[str]:
    text = re.sub(r"\[C\d+\]", "", text)
    text = re.sub(r"[#*_`>|]", " ", text)
    parts = re.split(r"(?<=[.!?])\s+|\n\s*[-\d]+[.)]?\s+|\n{2,}", text)
    out = []
    for p in parts:
        p = " ".join(p.split())
        if len(tokenize(p)) >= 4:
            out.append(p)
    return out


def tokenize(text: str) -> list[str]:
    words = re.findall(r"[a-zA-ZçğıöşüÇĞİÖŞÜ][a-zA-ZçğıöşüÇĞİÖŞÜ\-]+", text.lower())
    return [w for w in words if w not in STOP and len(w) > 2]


class _Vectorizer:
    def __init__(self, docs: list[str]):
        tokenized = [set(tokenize(d)) for d in docs]
        n = max(len(docs), 1)
        df = Counter(w for toks in tokenized for w in toks)
        self.idf = {w: math.log((1 + n) / (1 + c)) + 1 for w, c in df.items()}

    def vec(self, text: str) -> dict[str, float]:
        tf = Counter(tokenize(text))
        v = {w: c * self.idf.get(w, 1.0) for w, c in tf.items()}
        norm = math.sqrt(sum(x * x for x in v.values())) or 1.0
        return {w: x / norm for w, x in v.items()}


def _cos(a: dict, b: dict) -> float:
    if len(a) > len(b):
        a, b = b, a
    return sum(x * b.get(w, 0.0) for w, x in a.items())


def best_matches(candidates: list[str], reference: list[str]) -> list[tuple[str, str, float]]:
    vz = _Vectorizer(candidates + reference)
    ref_vecs = [vz.vec(r) for r in reference]
    out = []
    for c in candidates:
        cv = vz.vec(c)
        scores = [(_cos(cv, rv), r) for rv, r in zip(ref_vecs, reference)]
        score, ref = max(scores) if scores else (0.0, "")
        out.append((c, ref, round(score, 3)))
    return out


def claim_drift_index(rendering: str, h_claims: list[str], threshold: float = DEFAULT_THRESHOLD) -> dict:
    """CDI = share of atomic claims in a reader rendering not supported by the H layer."""
    cands = split_claims(rendering)
    matches = best_matches(cands, h_claims)
    unsupported = [m for m in matches if m[2] < threshold]
    cdi = len(unsupported) / len(cands) if cands else 0.0
    return {
        "n_claims": len(cands),
        "n_unsupported": len(unsupported),
        "cdi": round(cdi, 3),
        "threshold": threshold,
        "unsupported": [{"claim": c, "best_match": r, "score": s} for c, r, s in unsupported],
        "matches": [{"claim": c, "best_match": r, "score": s} for c, r, s in matches],
    }


def semantic_delta(before: str, after: str, threshold: float = DEFAULT_THRESHOLD) -> dict:
    """Claim-level difference between two texts (e.g. model draft -> final H text).

    retained = claims in ``after`` matched in ``before``; added = claims in
    ``after`` with no match; removed = claims in ``before`` with no match in
    ``after``. delta = (added + removed) / (claims in before + added).
    """
    b, a = split_claims(before), split_claims(after)
    fwd = best_matches(a, b) if b else [(c, "", 0.0) for c in a]
    back = best_matches(b, a) if a else [(c, "", 0.0) for c in b]
    added = sum(1 for m in fwd if m[2] < threshold)
    retained = len(a) - added
    removed = sum(1 for m in back if m[2] < threshold)
    denom = len(b) + added
    return {
        "retained": retained,
        "added": added,
        "removed": removed,
        "delta": round((added + removed) / denom, 3) if denom else 0.0,
    }


def _has(text: str, words) -> bool:
    low = f" {text.lower()} "
    return any(re.search(rf"\b{re.escape(w)}\b", low) for w in words)


def surface_check(before: str, after: str, threshold: float = ESCALATION_THRESHOLD) -> dict:
    """Decide whether an edit logged as 'surface' must be escalated to substantive.

    Escalation happens when the claim-level delta exceeds the threshold, or when
    the edit removes hedging and adds certainty (e.g. "may suggest" ->
    "demonstrates"), which changes what the paper claims even if few words move.
    """
    d = semantic_delta(before, after)
    hedge_shift = _has(before, HEDGES_WEAK) and not _has(after, HEDGES_WEAK) and _has(after, HEDGES_STRONG)
    # word-level change ratio as a second signal for short edits; a removed word
    # and an added word that are near-identical spellings count as a spelling fix
    tb, ta = Counter(tokenize(before)), Counter(tokenize(after))
    removed, added = list((tb - ta).elements()), list((ta - tb).elements())
    for r in list(removed):
        for a_ in added:
            if SequenceMatcher(None, r, a_).ratio() >= 0.8:
                removed.remove(r)
                added.remove(a_)
                break
    total = sum(tb.values()) + sum(ta.values()) or 1
    word_delta = round((len(removed) + len(added)) / total, 3)
    delta = max(d["delta"], word_delta)
    return {
        "semantic_delta": delta,
        "hedge_shift": hedge_shift,
        "escalated": bool(hedge_shift or delta > threshold),
        "threshold": threshold,
    }
