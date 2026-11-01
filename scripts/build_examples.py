"""Build the two example manuscripts.

1. examples/proposal      : this proposal, documented in its own format at LEM-1.
                             Records are author-assembled after the fact from the
                             writing session (human author + Claude), so they reach
                             LEM-1, not LEM-2.
2. examples/toy-analytic  : a small analytic task captured live by the capture
                             logger with the deterministic mock backend (LEM-2
                             mechanism demo).

Run once: `python scripts/build_examples.py`. It refuses to overwrite sealed logs.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from lem.backends import MockBackend  # noqa: E402
from lem.capture import CaptureLog, captured_call  # noqa: E402
from lem.hashing import sha256_file  # noqa: E402

CLAUDE = {"name": "Claude Opus 5.5", "version": "claude-opus-5-5",
          "provider": "Anthropic (claude.ai)", "open_weights": False}
AUTHOR_ASSEMBLED = {"source": "author-assembled",
                    "note": "Compiled after the session from the conversation record; not captured live."}


def write_json(path: Path, obj) -> None:
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


# --------------------------------------------------------------------------- proposal
def build_proposal() -> None:
    ex = ROOT / "examples" / "proposal"
    log = CaptureLog(ex / "P", source="author-assembled")
    if log.records():
        print("proposal: P layer already sealed, skipping")
        return

    steps = [
        ("2026-11-01T09:28:00+03:00", {
            "id": "I01", "type": "P_ideation", "model": CLAUDE, "capture": AUTHOR_ASSEMBLED,
            "prompt": ("makale çağrısı https://orgsci.org/ bu adrese bakar mısın buraya bir makale önerisi gönderelim, "
                       "fikir bilimin yayınlanmasında yeni yazım modeli IMRAD alternatifi, yapay zekanın yaptığı şeylerin "
                       "görünmediği okuyucularında yapay zekayla özetlettirince gördüğü kısımların olduğu diğer kısımların "
                       "promptlardan oluştuğu bir bilimsel yayın formatı sistemi tasarlıyorum. bu sayı için uygun olur mu? "
                       "editörlerin gözünden değerlendir."),
            "model_output": ("[Excerpt] Fit is partial as a 'new writing format'; strong if reframed as auditable provenance "
                             "for AI-enabled research. Proposed a three-layer structure: H (human claims), P (executable "
                             "prompts and model records), R (reader-side AI renderings, outside the record). Proposed a "
                             "claim-level measure of drift between reader summaries and author claims. Flagged risks: "
                             "reproducibility of reader-generated parts, 'AI slop' perception, missing organizational "
                             "framing, required Git prototype. Suggested Letter format as fallback."),
            "override_log": [
                {"proposal": "Reframe from a new writing format to auditable provenance of AI-enabled research",
                 "decision": "accepted", "author_note": "Author: 'Bunu bugüne yetiştireceğiz' (we will make the deadline today)."},
                {"proposal": "Three layers H / P / R formalizing the author's idea of prompt parts and reader-side AI summaries",
                 "decision": "accepted"},
                {"proposal": "Claim-level drift measure for reader renderings (later named CDI)", "decision": "accepted"},
                {"proposal": "Letter format as fallback", "decision": "accepted"},
            ],
        }),
        ("2026-11-01T09:34:00+03:00", {
            "id": "D01", "type": "P_drafting", "model": CLAUDE, "capture": AUTHOR_ASSEMBLED,
            "author_skeleton": "Bunu bugüne yetiştireceğiz, önce öneri metnini oluşturalım. + accepted decisions of I01.",
            "model_draft": {"redacted": True,
                            "reason": ("First full draft (sections Summary-7) was superseded in place and not archived. "
                                       "This gap is a known limitation of author-assembled LEM-1 records; the LEM-2 "
                                       "capture logger closes it.")},
            "final_ref": "H.md", "semantic_delta": None,
            "override_log": [
                {"proposal": "First full draft of the proposal", "decision": "rewritten",
                 "author_note": "Author issued revision directives extending the P layer to cognitive writing (see I02)."},
            ],
        }),
        ("2026-11-01T10:26:00+03:00", {
            "id": "I02", "type": "P_ideation", "model": CLAUDE, "capture": AUTHOR_ASSEMBLED,
            "prompt": ("[Author directive, condensed from Turkish] Revise LEM so that AI is auditable not only in data "
                       "analysis but in cognitive writing: (1) ideation and theory building, (2) structuring and drafting, "
                       "(3) mechanical editing. Section 1: extend 'invisible delegation' to ghost-thinking; add that "
                       "'we used ChatGPT' disclosures cannot tell whether the model fixed commas or built the thesis. "
                       "Section 2: add conceptual ideation loops, argument synthesis workflows and semantic delta to P; "
                       "add two-tier logging (substantive steps in full with override log; surface steps as meta-tags). "
                       "Section 3: add P_ideation and P_drafting step-types. Section 6: make measurable whether social "
                       "scientists use AI as idea generator or grammar assistant. Keep H/P/R intact; answer the call's "
                       "'AI slop' concern: the point is to prove editorial filtering of the model's cognitive input."),
            "model_output": ("[Excerpt] Assessed as fitting and strengthening. Raised six issues: (1) cognitive steps cannot "
                             "be validated by re-execution, so split P into executed vs traced steps; (2) author-kept logs "
                             "are self-report, so capture them automatically with hash chaining; (3) the surface/substantive "
                             "boundary must be enforced by a semantic-delta threshold with automatic escalation; (4) Section 4 "
                             "needs evidence for the new capabilities; (5) Summary, risks and ethics need updates (stigma risk, "
                             "redaction rule); (6) word limit."),
            "override_log": [
                {"proposal": "Analytic steps executed, cognitive steps traced", "decision": "accepted"},
                {"proposal": "Automatic hash-chained capture of records", "decision": "accepted"},
                {"proposal": "Escalate surface edits above a semantic-delta threshold", "decision": "accepted"},
                {"proposal": "Add evidence for cognitive steps to the planned studies", "decision": "accepted"},
                {"proposal": "Disclosure-stigma risk and redaction rule", "decision": "accepted"},
            ],
        }),
        ("2026-11-01T10:32:00+03:00", {
            "id": "I03", "type": "P_ideation", "model": CLAUDE, "capture": AUTHOR_ASSEMBLED,
            "prompt": ("Şimdi tüm sürecin kontrollü bir yapay zeka ortamında yürütülme zorunluluğu mu doğdu. bunu aşamalı "
                       "mı yapsak LEM 0 ve LEM 1 denebilir mi LEM 0 ilk hali LEM 1 yz makale diğer katkıların da görünür "
                       "olduğu hal, sen bunlara güzel isimler bularak ifade et bakalım nasıl duracak"),
            "model_output": ("[Excerpt] A controlled environment is not required if levels are staged. Separated scope "
                             "(what is logged) from assurance (how records are trusted) and proposed three levels: LEM-0 "
                             "Analytic Provenance, LEM-1 Cognitive Provenance, LEM-2 Attested Provenance (instrumented, "
                             "hash-sealed capture). Offered an alternative metaphor set (Glass Lab / Glass Desk / Sealed "
                             "Desk). Proposed comparing LEM-1 declarations with LEM-2 captured records as a study."),
            "override_log": [
                {"proposal": "Staged adoption (LEM-0, LEM-1)", "decision": "accepted",
                 "author_note": "Staging was the author's own proposal; the model extended it."},
                {"proposal": "Add a third level, LEM-2 Attested Provenance", "decision": "accepted"},
                {"proposal": "Names: Analytic / Cognitive / Attested Provenance", "decision": "accepted"},
                {"proposal": "Alternative names: Glass Lab / Glass Desk / Sealed Desk", "decision": "rejected"},
                {"proposal": "Study comparing declared (LEM-1) and captured (LEM-2) contribution", "decision": "accepted"},
            ],
        }),
        ("2026-11-01T10:35:00+03:00", {
            "id": "D02", "type": "P_drafting", "model": CLAUDE, "capture": AUTHOR_ASSEMBLED,
            "author_skeleton": "Directives of I02 and decisions of I03: 'Tablodaki ad setleri uygun ... son halini oluştur'.",
            "model_draft": "Revised proposal (Summary, sections 1-7, references). Full text kept in the proposal document.",
            "model_draft_ref": "Proposal document, revision of 2026-11-01 10:35 (Istanbul)",
            "final_ref": "H.md", "semantic_delta": None,
            "override_log": [
                {"proposal": "Revised full draft", "decision": "accepted",
                 "author_note": "Accepted pending the author's own revision. Run `lem delta` on draft vs. final H after editing."},
            ],
        }),
        ("2026-11-01T10:44:00+03:00", {
            "id": "I04", "type": "P_ideation", "model": CLAUDE, "capture": AUTHOR_ASSEMBLED,
            "prompt": "github a sen yükle, Lisans uygun, Lem-manuscript uygun, bu öneriyi koyalım güzel olur",
            "model_output": ("[Excerpt] Proposed a repository reviewers can run in minutes (offline mode, open-weight option, "
                             "honest STATUS file) and proposed documenting the proposal itself in LEM format as the "
                             "reference manuscript."),
            "override_log": [
                {"proposal": "Use this proposal as the reference manuscript (self-documentation)", "decision": "accepted"},
                {"proposal": "MIT licence for code, CC BY 4.0 for documents", "decision": "accepted"},
                {"proposal": "Repository name lem-manuscript", "decision": "accepted"},
            ],
        }),
    ]
    paths = []
    for ts, rec in steps:
        log.append(rec, timestamp=ts)
    for f in sorted((ex / "P").glob("*.json")):
        paths.append(f"P/{f.name}")

    claims = [
        {"id": "C1", "origin": "model", "p_steps": ["I01", "D01"],
         "text": "IMRAD assumes one authorial voice: everything in the text is attributed to the named authors, and methods are described in prose rather than executed."},
        {"id": "C2", "origin": "author", "p_steps": ["I02"],
         "text": "A statement such as 'we used ChatGPT' does not tell a reader whether the model corrected commas or built the central thesis (ghost-thinking)."},
        {"id": "C3", "origin": "co-constructed", "p_steps": ["I01"],
         "text": "LEM replaces the single-voice IMRAD article with three separable layers: Human, Process and Reader."},
        {"id": "C4", "origin": "model", "p_steps": ["I01"],
         "text": "The Claim Drift Index is the share of atomic claims in a rendering that are unsupported by, or contradict, the H layer."},
        {"id": "C5", "origin": "model", "p_steps": ["I02"],
         "text": "Analytic steps are validated by re-execution; cognitive steps are validated by traceability of what the model proposed and what the author accepted, rejected or rewrote."},
        {"id": "C6", "origin": "author", "p_steps": ["I02"],
         "text": "Two-tier logging records substantive cognitive steps in full with an override log and surface edits only as meta-tags."},
        {"id": "C7", "origin": "model", "p_steps": ["I02"],
         "text": "A surface edit whose semantic delta exceeds a threshold, such as turning 'may suggest' into 'demonstrates', is escalated to substantive automatically."},
        {"id": "C8", "origin": "co-constructed", "p_steps": ["I03"],
         "text": "LEM is adopted in three conformance levels: LEM-0 Analytic Provenance, LEM-1 Cognitive Provenance and LEM-2 Attested Provenance."},
        {"id": "C9", "origin": "model", "p_steps": ["I03"],
         "text": "LEM-2 adds assurance, not scope: records are captured automatically and sealed in a hash chain so they cannot be curated after the fact."},
        {"id": "C10", "origin": "model", "p_steps": ["I03"],
         "text": "Comparing LEM-1 declarations with LEM-2 captured records shows how far self-declared AI contribution departs from captured contribution."},
        {"id": "C11", "origin": "author", "p_steps": ["I02"],
         "text": "LEM makes it measurable whether social scientists use AI as an idea generator or only as a grammar assistant."},
        {"id": "C12", "origin": "co-constructed", "p_steps": ["I02", "D02"],
         "text": "The override log is the evidence that a human, not the model, decided what the paper claims."},
        {"id": "C13", "origin": "model", "p_steps": ["I04"],
         "text": "The reference manuscript in the repository is this proposal documented in its own format at LEM-1."},
    ]
    write_json(ex / "claims.json", claims)
    write_json(ex / "manifest.json", {
        "lem_version": "0.1",
        "conformance_level": "LEM-1",
        "title": "Executable Manuscripts: An Auditable Layered Architecture for Publishing AI-Enabled Organizational Research",
        "authors": ["[Author name, affiliation]"],
        "h_layer": "H.md",
        "h_hash": sha256_file(ex / "H.md"),
        "claims": "claims.json",
        "p_steps": paths,
        "r_layer": ["R/summary_faithful.md", "R/summary_drifted.md"],
        "notes": ("Written by a human author with Claude (Anthropic) in one session on 2026-11-01. P records are "
                  "author-assembled from the conversation, so the manuscript conforms to LEM-1, not LEM-2. Model outputs "
                  "are stored as excerpts; one superseded draft is marked as redacted with its reason."),
    })
    print(f"proposal: sealed {len(paths)} P-steps, {len(claims)} claims")


# --------------------------------------------------------------------------- toy analytic (LEM-2 mechanism)
TOY_INPUTS = [
    "I asked the assistant to brainstorm three hypotheses about remote-work trust.",
    "The model wrote the first draft of the discussion section from my bullet points.",
    "I only used it to fix grammar and spelling in the abstract.",
    "We met the department head to discuss teaching loads.",
    "It suggested a theory linking psychological safety to voice behaviour.",
    "I pasted my outline and it produced two paragraphs for the literature review.",
]
TOY_PROMPT = ("Classify how AI was used in this statement from a researcher. "
              "Answer with one label: idea-generation, drafting, editing, none.")


def build_toy() -> None:
    ex = ROOT / "examples" / "toy-analytic"
    (ex / "inputs.txt").write_text("\n".join(TOY_INPUTS) + "\n", encoding="utf-8")
    log = CaptureLog(ex / "P", source="capture-logger")
    if log.records():
        print("toy-analytic: P layer already sealed, skipping")
        return
    backend = MockBackend()
    for i, text in enumerate(TOY_INPUTS, start=1):
        captured_call(log, backend, f"A{i:02d}", TOY_PROMPT, text, input_ref=f"inputs.txt#L{i}", seed=42)
    recs = log.records()
    labels = [r["output"] for r in recs]
    counts = {l: labels.count(l) for l in sorted(set(labels))}
    h = (
        "# Toy analytic example (LEM-2 mechanism demo)\n\n"
        "*H layer. Six researcher statements were classified by a model to show how analytic P-steps are captured "
        "and re-executed. The backend is a deterministic mock, not an LLM; replace it with `--backend ollama:<model>` "
        "to run a real open-weight model.*\n\n"
        f"Of six statements, {counts.get('idea-generation', 0)} describe AI as an idea generator, "
        f"{counts.get('drafting', 0)} describe drafting, {counts.get('editing', 0)} describe editing only, "
        f"and {counts.get('none', 0)} describe no AI use. [C1]\n\n"
        "Every classification can be re-executed from its sealed record, and any change to a record breaks the hash chain. [C2]\n"
    )
    (ex / "H.md").write_text(h, encoding="utf-8")
    write_json(ex / "claims.json", [
        {"id": "C1", "origin": "author", "p_steps": [r["id"] for r in recs],
         "text": "The six statements split into idea generation, drafting, editing and no AI use as reported."},
        {"id": "C2", "origin": "author", "p_steps": [r["id"] for r in recs],
         "text": "Every classification can be re-executed from its sealed record."},
    ])
    write_json(ex / "manifest.json", {
        "lem_version": "0.1",
        "conformance_level": "LEM-2",
        "title": "Toy analytic example (LEM-2 mechanism demo)",
        "authors": ["LEM toolkit"],
        "h_layer": "H.md",
        "h_hash": sha256_file(ex / "H.md"),
        "claims": "claims.json",
        "p_steps": [f"P/{f.name}" for f in sorted((ex / "P").glob("*.json"))],
        "notes": "Captured live by lem.capture with the deterministic mock backend.",
    })
    print(f"toy-analytic: captured {len(recs)} P-steps, labels {counts}")


if __name__ == "__main__":
    build_proposal()
    build_toy()
