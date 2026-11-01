# Status (v0.1, 1 November 2026)

An honest account of what this proof of concept does today and what the proposal commits to build.

| Component | Status | Notes |
| --- | --- | --- |
| Schema v0.1 (manifest, claims, 4 P step-types, redaction) | Working | JSON Schema draft 2020-12 |
| Hash chain (seal, verify, tamper detection) | Working | SHA-256 over canonical JSON; tested |
| Validator (schema, chain, H integrity, anchors, level rules) | Working | LEM-2 rejects author-assembled records |
| Capture logger (LEM-2) | Working, minimal | Wraps model calls for analytic steps; capture of chat-style ideation and drafting sessions is planned |
| Re-execution | Working with mock backend; Ollama backend experimental | Real cross-model reproducibility study is Study 1 |
| Claim Drift Index | Working, lexical baseline | TF-IDF matching detects *unsupported* claims; *contradiction* detection needs the planned LLM/NLI judge |
| Semantic delta and surface escalation | Working, lexical baseline | Hedge-shift rule plus claim- and word-level delta; thresholds not yet calibrated against human coders |
| Provenance report | Working | Origins in `claims.json` are assigned by the author and are themselves a LEM-1 declaration |
| Reference manuscript (this proposal, LEM-1) | Working | Model outputs stored as excerpts; one superseded draft visibly redacted |
| Reader renderings in `R/` | Synthetic | Written for the demo, not produced by readers' tools |
| Interactive viewer (click a claim, see its record) | Planned | |
| LLM judge, human-coder validation of CDI and delta | Planned | Proposal, section 5 |
| Studies 1–4 | Planned | January–May 2027 |

## Known limitations

* The proposal example was drafted with a proprietary model (Claude). The toolkit itself depends only on open components, and re-execution targets open-weight models.
* At LEM-1, records are compiled by the authors and can be incomplete; Study 4 is designed to measure that gap.
* Lexical matching undercounts paraphrased support and cannot see negation; numbers reported here are illustrations of the mechanism, not findings.
