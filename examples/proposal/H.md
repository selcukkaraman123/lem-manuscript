# Executable Manuscripts: An Auditable Layered Architecture for Publishing AI-Enabled Organizational Research

*H layer (Human). Proposal to the Organization Science special issue "AI-Assisted Frontiers in Organizational Science". Claim anchors such as [C1] link sentences to the claim index (`claims.json`) and, through it, to the P-layer records that shaped them.*

## Summary

We propose the **Layered Executable Manuscript (LEM)**, a publication architecture that replaces the single-voice IMRAD article with three separable layers. [C3] The first is a fixed Human layer of claims, theory and accountable interpretation. The second is a machine-readable Process layer that records how AI contributed to the work: not only analytic steps such as coding and classification, but also the cognitive work of writing — ideation, theory building, literature synthesis and drafting. The third is a Reader layer of AI-rendered views, such as summaries, translations or method walkthroughs, which readers generate on demand and which never count as part of the scholarly record. LEM is adopted in three conformance levels: LEM-0 (Analytic Provenance), LEM-1 (Cognitive Provenance) and LEM-2 (Attested Provenance). [C8]

IMRAD was designed for research written by people. In AI-enabled research, much of the work — coding text, generating candidate hypotheses, drafting analyses — is done by models whose role readers cannot see or audit. LEM makes that division of labor explicit and checkable.

We will (1) release an open schema and toolkit, (2) write a demonstration manuscript at LEM-2 that re-expresses a published organizational study, and (3) test whether LEM improves reproducibility, the fidelity of AI-rendered reading, reviewers' ability to locate AI judgment, and the match between declared and captured AI contribution. The contribution is both infrastructure and a boundary-setting study of where AI enters scientific thinking and where AI-mediated reading drifts from authors' claims.

## 1. Problem: the article format hides where AI judgment enters

IMRAD became the dominant structure of empirical articles over the twentieth century (Sollaci & Pereira, 2004). It assumes one authorial voice: everything in the text is attributed to the named authors, and methods are described in prose rather than executed. [C1] AI-enabled research breaks both assumptions in three ways.

- **Invisible delegation and ghost-thinking.** Models now code qualitative data and generate measures. They also take part in intellectual work: proposing hypotheses, synthesizing literatures, constructing arguments and drafting paragraphs. We call this hidden cognitive contribution *ghost-thinking*: model reasoning that shapes a paper's argument without appearing in its record. A statement such as "we used ChatGPT" does not tell a reader whether the model corrected commas or built the central thesis. [C2] A methods paragraph on LLM classification does not show the prompts, model version, discarded outputs, or where authors overrode the model. This is the zone the call names: where AI systems drift, obscure judgment, or undermine validity.
- **Volume without auditability.** LLM-modified text is spreading rapidly in the scientific literature (Liang et al., 2024). Disclosure statements are coarse and unverifiable. Journals cannot tell AI-heavy, low-engagement work from carefully directed AI-enabled research, because the format records neither.
- **AI-mediated reading.** Readers increasingly meet papers through AI summaries. Those summaries can compress, distort or invent claims (Messeri & Crockett, 2024). The scholarly record has no reference point to measure that drift against, so no one owns it.

Prior responses each solve one piece. Executable notebooks make code runnable (Knuth, 1984; Donoho, 2010); open-science standards make data reusable (Nosek et al., 2015; Wilkinson et al., 2016); contributor taxonomies make human credit explicit (Allen et al., 2014). None separates human from model contributions inside the article, and none measures reader-side AI rendering.

## 2. Intended contribution: the Layered Executable Manuscript

LEM splits an article into three layers. Each layer has a different author, status and test of validity.

| Layer | Contents | Who is accountable | Status in the record | Validity test |
| --- | --- | --- | --- | --- |
| **H — Human** | Research question, theory, claims, interpretation, decisions to accept or override model output | Named authors | Fixed, citable, peer-reviewed | Is the argument sound? |
| **P — Process** | *Analytic steps:* prompts, model and version, parameters, agent workflow graph, input data references, hashed reference outputs. *Cognitive steps:* conceptual ideation loops (hypothesis and theory building), argument synthesis workflows, drafting records with a semantic delta (diff) between author input, model draft and final H text. Human override log throughout. | Authors, for design and every acceptance decision; the model, for execution | Fixed, versioned, executable or traceable | *Analytic:* does re-execution reproduce reference outputs within tolerance? *Cognitive:* can each H claim be traced to its origin — author, model, or model proposal transformed by the author? |
| **R — Reader** | Summaries, translations, method walkthroughs, critiques generated by readers' own AI tools | No one; generated at reading time | Not part of the record | How far does it drift from H? |

Three design principles follow.

1. **Every claim in H is anchored.** Each claim carries an identifier linking it to the P-layer steps behind it, analytic or cognitive. A reader or reviewer can trace any sentence to the prompt, model and output that produced its evidence or shaped its argument.
2. **Analytic steps are executed; cognitive steps are traced.** An analytic P-step is a machine-readable record that should reproduce its hashed reference output when re-run on a pinned open-weight model. Cognitive steps are generative and are not expected to reproduce. Their validity is provenance: the record shows what the model proposed and what the author accepted, rejected or rewrote, measured as a semantic delta. [C5]
3. **R is measured against H.** Because H is a fixed set of anchored claims, any AI-rendered view can be scored for claim-level fidelity. We call this the **Claim Drift Index (CDI)**: the share of atomic claims in a rendering that are unsupported by, or contradict, H. [C4] It adapts atomic-fact precision methods from NLP (Min et al., 2023). The same claim-matching engine computes the semantic delta in drafting records.

**Two-tier logging.** To keep the cost of logging in line with what is at stake, P records cognitive steps in two tiers. *Substantive steps* — ideation, literature synthesis, argument construction and drafting — are logged in full: prompt, model output, and an override log showing which parts the author accepted, rejected or rewrote. *Surface steps* — spelling, grammar and tone calibration only — are logged as a meta-tag (model and purpose of the edit), not as full text. [C6] The boundary is enforced, not self-declared. If a surface edit's semantic delta exceeds a set threshold, for example turning "may suggest" into "demonstrates", the step is escalated to substantive automatically. [C7]

The aim is not to document authors' reliance on model output. It is to show how the model's cognitive contribution passed through the author's editorial judgment. The override log is the evidence that a human, not the model, decided what the paper claims. [C12]

**Conformance levels.** LEM is adopted in graduated levels, following the tiered logic of the TOP Guidelines (Nosek et al., 2015).

| Level | Scope | Assurance |
| --- | --- | --- |
| **LEM-0 — Analytic Provenance** | Analytic P-steps only (coding, classification, extraction) | Re-execution |
| **LEM-1 — Cognitive Provenance** | LEM-0 plus ideation, theory building, synthesis and drafting, with two-tier logging | Records assembled by the authors |
| **LEM-2 — Attested Provenance** | Same scope as LEM-1 | Records captured automatically by an instrumented research environment and sealed in a hash chain, so they cannot be curated after the fact |

LEM-2 adds assurance, not scope. [C9] No level requires the one above it. A journal can require LEM-0, encourage LEM-1, and reserve LEM-2 for papers where AI's cognitive role is itself under scrutiny.

The scientific contribution is not a template. It is a way to **observe the human–AI division of labor in research**, analytic and cognitive, which today cannot be studied because the record does not capture it. LEM makes four open questions answerable: how reproducible AI-executed steps are across models, how much meaning AI-mediated reading loses, whether reviewers can locate AI judgment when the format exposes it, and how far declared AI contribution departs from captured contribution.

## 3. Work completed

The submitted repository contains a working proof of concept with five parts: the LEM schema v0.1 with four P step-types (`P_analytic`, `P_ideation`, `P_drafting`, `P_surface`); a reference manuscript, which is this proposal documented in its own format at LEM-1; a re-execution script; a claim-matching prototype that computes the CDI and the semantic delta; and a capture logger that seals model calls in a hash chain (LEM-2 prototype). [C13]

## 4. Planned work (January–May 2027)

We will run four linked studies on one demonstration case. The case is a published organizational study with open data and a text-analytic component that can be re-done with AI-enabled coding: [target article, journal, year, data source].

**Study 1 — Re-expression and reproducibility.** We rebuild the target study's AI-enabled analysis as a LEM manuscript. We re-execute every analytic step across at least three open-weight models, two versions each, and repeated seeds. Outcomes: exact-match rate, semantic agreement with reference outputs, and — most important — whether H-layer conclusions survive the variation. We also write the demonstration manuscript itself at LEM-2: every ideation, synthesis and drafting step is captured by the logging environment, which shows that the highest level is workable in practice.

**Study 2 — Fidelity of AI-mediated reading.** We generate reader-layer renderings of the same study in two formats: (a) the conventional IMRAD PDF and (b) the LEM manuscript. We use several models and common reader prompts (summarize, extract the findings, explain the method, translate to Turkish). We compute the CDI for each rendering and test whether LEM's anchored claims reduce drift. Expected result: lower CDI for LEM, with drift concentrated in hedged and conditional claims.

**Study 3 — Reviewer experiment.** We recruit [N ≈ 60] reviewers from management and information systems. In a between-subjects design, each evaluates the same study in IMRAD or LEM form. Measures: accuracy at identifying where AI judgment entered the analysis, accuracy at attributing a given claim to author or model origin, detection of a seeded AI error, time on task, and confidence.

**Study 4 — Declared versus captured contribution.** [N ≈ 20] researchers complete a short writing task with AI inside the LEM-2 environment. They then independently prepare a LEM-1 declaration of the same work. Comparing the two shows how far self-declared AI contribution departs from captured contribution, and in which direction. [C10]

## 5. Key risks

The main risk is that LLM non-determinism makes analytic P-steps irreproducible even on pinned models. We treat this as a finding to report, not a failure. Further risks — self-curated logs at LEM-1, disclosure stigma, circularity of an LLM judge, adoption burden and model deprecation — and their mitigations are listed in the full proposal.

## 6. What changes for organizational and social science if this succeeds

Science is itself an organized activity: journals, reviewers and authors coordinate through shared formats, and the format decides what is visible, rewarded and held accountable. LEM makes it measurable whether social scientists use AI as an idea generator or only as a grammar assistant: through the share of H claims traceable to `P_ideation`, the rate at which authors reject or rewrite model proposals, and the semantic delta between model drafts and final text. [C11] The cognitive division of labor in research writing becomes transparent and quantifiable.

## References

See the full proposal. Key sources: Allen et al. (2014); Bail (2024); Dell'Acqua et al. (2023); Donoho (2010); Girotra, Terwiesch & Ulrich (2010); Knuth (1984); Lebo et al. (2013); Liang et al. (2024); March (1991); Messeri & Crockett (2024); Min et al. (2023); Nosek et al. (2015); Ouyang et al. (2025); Sollaci & Pereira (2004); Wilkinson et al. (2016).
