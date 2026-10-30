# tether -- the general agent

Branch `general-agent`. The agent itself, with no domain attached. The same code, applied to
ARC-AGI-3, is the branch `arc-solver-agent`.

## What the agent is

One agent running one loop: it perceives a world, predicts what it will see next, acts, and
measures what its prediction missed. The miss (the **residual**) is kept per object slot and is
never averaged across slots. A new term enters the agent's model only when it pays for itself in
a compression bargain (`|phi| + |R|phi| < |R|`): the term plus what it still fails to explain
must cost less than the miss it explains.

    PERCEIVE -> ROUTE -> MINT -> ACCEPT -> SETTLE -> PROMOTE -> IMPORT -> REPEAT

The loop has no branch on problem type. Every stage writes to a ledger, and a separate checker
(`gate.py`) reads that ledger and can fail the run. The checker imports nothing from the loop, so
the thing it checks cannot talk it round.

**The agent is the prize. Winning is not.** The deliverable is an agent that reasons through
problems it was never told about and can say how and why, in its own record, in terms a reader
can check. A change that makes it better and its reasoning unreadable is a loss.

## The agent decides intent; the interface carries it out

The agent reasons in what it wants to be true, never in buttons. Its intents are said in the
grammar's own primes (`ELICIT`, `TOUCH`, `BE_AT`, `BECOME`, `DISTINGUISH`).

- **The action side is `interface.py`.** It translates an intent into whatever actions the world
  offers (`Interface.realise`), and reports what each press did back up as capability
  (`Interface.audit`). It may translate and report. It may not choose between goals, rank
  intents, or withhold a capability the world offers. Its table of what each action does starts
  empty and is filled only by acting.
- **The input side is `world.py`'s `Env` contract.** A world is an adapter that fills it:
  substrate, environment, actors, currency, ground, slots, atoms, transform, actions, alphabet. An
  adapter that cannot fill it fails at construction.

These two layers are the swappable parts. The agent decides what it intends; the layers decide how
that is carried out, depending on the inputs and actions a world provides. The reasoning above them
does not change with the world: a different world brings a different adapter and a different set of
actions, and the agent's intents are carried out with whatever it provides. The tree carries a
symbolic world (`world.py`), a grid world (`gridworld.py`), and the ARC-AGI-3 adapter and harness,
which are identical on both branches (see `arc-solver-agent`'s README).

## What ships, and what does not

- **Ships:** the code, and the library (`library/`): atoms, molecules, relations and grammar.
  The library is the agent's inheritance: what it can say. It holds no answer to any problem. A
  missing or partial `library/` stops the agent at startup and names each missing file.
- **Does not ship:** anything learned. The agent starts with its inherited library and no
  experience of its own. What it learns is written to a lineage folder outside the repository (one
  generation file per run, plus its memory store), which starts empty. No lineage, learned library
  or run ledger is ever committed. Two seat-side records are: `docs/log_index/` (a copy of the run
  index -- one lossy summary row per run ledger -- with its pins and removals, committed after each
  indexing box by ruling, and read by `tests/test_log_index.py`) and `docs/TOMBSTONES/` (the record
  of files removed on Isaiah's word, what they were and why). Neither holds anything the agent
  learned or reads.

## From a fresh clone

Python 3.13 (`pyproject.toml`: `>=3.13,<3.14`). `requirements.lock` pins the whole runtime; install
it with `--no-deps` so nothing else is resolved.

    git clone -b general-agent https://github.com/IsaiahN/tether.git
    cd tether
    python -m venv .venv
    .venv/Scripts/python.exe -m pip install --no-deps -r requirements.lock   # bin/python off Windows

## The checks

Run from the repository root, one at a time, without writing bytecode:

    export PYTHONDONTWRITEBYTECODE=1                    # a POSIX shell; Git Bash on Windows
    .venv/Scripts/python.exe -m ruff check .
    .venv/Scripts/python.exe -B tests/test_gate.py
    .venv/Scripts/python.exe -B tests/test_entry.py
    .venv/Scripts/python.exe -B tests/test_gate_ledger.py
    .venv/Scripts/python.exe -B tests/test_arm_modules.py
    .venv/Scripts/python.exe -B conform/arms.py

Each prints its own result line and exits 0 when it passes. `tests/test_gate.py` checks the
checker itself: one planted defect per check, and every defect must be caught.

## Why it is whitebox

Because the agent predicts explicitly, its model is readable. Because the residual is an object,
the cause and effect it perceived is readable. Because minting is an inspectable event, the moment
of discovery, or its absence, is a diagnosis rather than a mystery.

## The objection to pre-empt

**A hand-authored library of composable predicates is Cyc.** The difference is the arbiter: Cyc's
predicates were graded by their authors; here every term is graded by a ground the library cannot
move. That is checkable in three places:

- **Nothing scores itself.** Coverage, terms minted and compression achieved are internal to the
  frame and are not evidence.
- **Priors are inheritance, not answers.** The library holds human priors (atoms and
  recipes) the agent starts with, the way an animal starts with its instincts; none is
  written for a particular problem.
- **The ablation is a procedure.** Back up the library, verify the backup, wipe it, and re-run
  (`TETHER_LIBRARY_REQUIRED=0` lets the agent start without it). If a result survives, the agent
  composed it; if it disappears, the library was carrying it.
