"""Regenerate everything in reports/ so reviewers can read results without running code."""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from lem.claims import claim_drift_index, surface_check  # noqa: E402
from lem.cli import _h_claims  # noqa: E402
from lem.provenance import provenance  # noqa: E402
from lem.reexecute import reexecute  # noqa: E402
from lem.validate import validate  # noqa: E402

OUT = ROOT / "reports"
OUT.mkdir(exist_ok=True)
P = ROOT / "examples" / "proposal"
T = ROOT / "examples" / "toy-analytic"


def dump(name, obj):
    (OUT / name).write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def rel(obj):
    """Replace absolute paths with repository-relative ones."""
    s = json.dumps(obj, ensure_ascii=False).replace(str(ROOT) + "/", "")
    return json.loads(s)


dump("validate_proposal.json", rel(validate(P)))
dump("validate_toy-analytic.json", rel(validate(T)))
dump("reexecute_toy-analytic_mock.json", rel(reexecute(T, "mock")))
ref = _h_claims(str(P))
cdi = {}
for name in ("summary_faithful", "summary_drifted"):
    r = claim_drift_index((P / "R" / f"{name}.md").read_text(encoding="utf-8"), ref)
    r.pop("matches")
    cdi[name] = r
dump("cdi_proposal.json", cdi)
dump("provenance_proposal.json", provenance(P))
cases = {
    "spelling_fix": ("The resuls suggest that trust mediates the efect of remote work on voice.",
                     "The results suggest that trust mediates the effect of remote work on voice."),
    "hedge_to_certainty": ("These results may suggest that trust mediates the effect.",
                           "These results demonstrate that trust mediates the effect."),
    "claim_replaced": ("Trust mediates the effect.",
                       "Our data show that trust has no effect on voice in hybrid teams."),
}
dump("surface_check_cases.json", {k: {"before": b, "after": a, **surface_check(b, a)} for k, (b, a) in cases.items()})
print("reports written to", OUT)
