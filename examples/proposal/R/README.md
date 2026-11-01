# R layer (Reader) — demonstration renderings

These two files are **synthetic reader renderings written for the demonstration**. They are not outputs of a real reader's AI tool and are not part of the scholarly record.

* `summary_faithful.md` restates claims that appear in the H layer.
* `summary_drifted.md` keeps the first sentence but then adds four claims that the H layer never makes (adoption by journals, a quality verdict, a pilot result, a policy recommendation).

Run `python -m lem cdi examples/proposal examples/proposal/R/summary_drifted.md` to see which claims the Claim Drift Index flags.
