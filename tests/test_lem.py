import copy
import json
import shutil
from pathlib import Path

from lem.claims import claim_drift_index, semantic_delta, surface_check
from lem.hashing import verify_chain
from lem.provenance import provenance
from lem.reexecute import reexecute
from lem.validate import load, validate

ROOT = Path(__file__).resolve().parent.parent
PROPOSAL = ROOT / "examples" / "proposal"
TOY = ROOT / "examples" / "toy-analytic"


def test_examples_validate():
    assert validate(PROPOSAL)["valid"]
    assert validate(TOY)["valid"]


def test_tampering_breaks_chain():
    _, steps, _, _ = load(PROPOSAL)
    assert verify_chain(steps) == []
    tampered = copy.deepcopy(steps)
    tampered[2]["override_log"][0]["decision"] = "rejected"
    problems = verify_chain(tampered)
    assert any("hash mismatch" in p for p in problems)


def test_deleting_a_record_breaks_chain():
    _, steps, _, _ = load(PROPOSAL)
    problems = verify_chain(steps[:1] + steps[2:])
    assert any("prev_hash" in p for p in problems)


def test_editing_h_requires_reseal(tmp_path):
    dst = tmp_path / "m"
    shutil.copytree(PROPOSAL, dst)
    with open(dst / "H.md", "a", encoding="utf-8") as fh:
        fh.write("\nAn unsealed sentence.\n")
    r = validate(dst)
    assert not r["valid"]
    assert any("H layer" in e for e in r["errors"])


def test_lem2_rejects_author_assembled(tmp_path):
    dst = tmp_path / "m"
    shutil.copytree(PROPOSAL, dst)
    m = json.loads((dst / "manifest.json").read_text(encoding="utf-8"))
    m["conformance_level"] = "LEM-2"
    (dst / "manifest.json").write_text(json.dumps(m), encoding="utf-8")
    r = validate(dst)
    assert not r["valid"]
    assert any("LEM-2 requires" in e for e in r["errors"])


def test_reexecute_mock_exact():
    r = reexecute(TOY, "mock")
    assert r["n_analytic_steps"] == 6
    assert r["exact_match_rate"] == 1.0


def test_cdi_separates_faithful_from_drifted():
    from lem.cli import _h_claims
    ref = _h_claims(str(PROPOSAL))
    good = claim_drift_index((PROPOSAL / "R" / "summary_faithful.md").read_text(encoding="utf-8"), ref)
    bad = claim_drift_index((PROPOSAL / "R" / "summary_drifted.md").read_text(encoding="utf-8"), ref)
    assert good["cdi"] < bad["cdi"]
    assert bad["n_unsupported"] >= 3


def test_surface_check_hedge_escalation():
    before = "These results may suggest that trust mediates the effect."
    after = "These results demonstrate that trust mediates the effect."
    r = surface_check(before, after)
    assert r["hedge_shift"] and r["escalated"]


def test_surface_check_spelling_not_escalated():
    before = "The resuls suggest that trust mediates the efect of remote work on voice."
    after = "The results suggest that trust mediates the effect of remote work on voice."
    r = surface_check(before, after)
    assert not r["hedge_shift"]
    assert not r["escalated"]


def test_semantic_delta_identity_and_change():
    t = "Trust mediates the effect of remote work on voice. Managers shape psychological safety in teams."
    assert semantic_delta(t, t)["delta"] == 0.0
    d = semantic_delta(t, t + " Hybrid schedules reduce informal knowledge sharing among new employees.")
    assert d["added"] == 1


def test_provenance_report():
    r = provenance(PROPOSAL)
    assert set(r["claims_by_origin"]) <= {"author", "model", "co-constructed"}
    assert "rejected" in r["override_decisions"]
