# tether

An agent-level decision architecture. The deliverable is **an agent that can say when an
answer is out of reach instead of confabulating one** — and that can show why, in its own
record, in terms a reader can check.

**The agent is the prize. Winning is not.** A black box that wins teaches nothing.

## The loop

One uniform per-step loop, no branching on problem type:

    PERCEIVE → ROUTE → MINT → ACCEPT → SETTLE → PROMOTE → IMPORT → REPEAT

The agent predicts, measures what its prediction missed (the **residual**, indexed per object
slot and never averaged across them), and mints a new term only when the term pays for itself
under a declared code — `|φ| + |R|φ| < |R|`. Three guards gate the mint (support,
reachability, novelty); the compression bargain settles it afterwards.

Every stage writes to a ledger. A separate checker reads that ledger and can fail the run.
**The checker imports nothing from the loop**, so it cannot be talked round by the thing it
is checking.

## Why it is whitebox

Legibility is not a presentation choice here, it is the instrument. Because the model
predicts explicitly, it is readable. Because the residual is an object, the cause-and-effect
the agent perceived is readable. Because minting is an inspectable event, the moment of
discovery — or its absence — is a diagnosis rather than a mystery.

**A change that makes the agent better but makes its reasoning unreadable is a loss, not a
win.**

## The objection to pre-empt

**A hand-authored library of composable knowledge predicates is Cyc.**

The answer is that **Cyc's ontology was graded by its authors, and these are graded by a
ground that does not update.** Cyc's predicates were correct when the people who wrote them
agreed they were; there was no external arbiter that could return a verdict they had not
anticipated. Here the arbiter is the environment, it is fixed before the agent starts, and it
returns the same verdict regardless of what the library says it should.

That distinction is load-bearing rather than rhetorical, and the repository makes it
checkable in three places:

- **Nothing scores itself.** A frame cannot be scored with a quantity it produces. Coverage,
  terms minted and compression achieved are frame-internal and are explicitly disqualified as
  evidence.
- **Priors enter under a stated rule, or not at all.** A prior is admitted only if the loop
  cannot run without it, or the agent minted a crude version first and it is being promoted.
  **Never because it would help on a particular problem** — that is the one move that encodes
  an answer, and once made, no amount of testing can detect it afterwards.
- **The ablation is runnable.** Back up the library, verify the backup, wipe it, re-run. If
  the result survives, the agent composed it. If it disappears, the library was carrying the
  answer and the agent was retrieving rather than reasoning.

## Running it

    .venv/Scripts/python.exe demo.py              # the whole loop, end to end
    .venv/Scripts/python.exe gate.py runs/demo.jsonl
    .venv/Scripts/python.exe test_gate.py         # the gate's checks, one defect each
    .venv/Scripts/python.exe -m ruff check .

`demo.py` prints what it learned, what it refused to claim, and where it stopped — including
the difference between *I ran out of budget* and *this is not reachable at this depth*, which
are different statements and only one of them is strong.
