# tether — a general learning agent

A CPU-only agent that **teaches itself**. It is given no model of any world and no answers. It
watches, predicts, acts, and keeps only the ideas that the world pays for. The ideas it keeps are
small programs in a typed language, so it builds its own vocabulary and then builds on it. Every
step is written to a record that a separate checker can fail.

It is an instance of **The Tether** architecture: Isaiah Nwukor's account of how intelligence
grows by mapping a world against a ground it cannot argue with.

- *Arrival of the Fittest: The Tether Architecture*:
  [Medium](https://medium.com/@IsaiahNwukor/arrival-of-the-fittest-the-tether-architecture-1de7edf641ec)
  · [Substack](https://adventuresinml.substack.com/p/arrival-of-the-fittest-the-tether)
- The figures it is built from are in [`figures/`](figures/), with the formula,
  [`figures/THE_FORMULA.md`](figures/THE_FORMULA.md).

## The four branches

- **[`core`](https://github.com/IsaiahN/tether/tree/core)**: the minimal kernel. The Tether loop,
  gate and abstention on a toy symbolic world, about 1,600 lines. Read this first to see the
  architecture whole.
- **[`general-agent`](https://github.com/IsaiahN/tether/tree/general-agent)** (this one): the
  full general learning agent. Domain-agnostic: the library of ~4,000 human-prior entries, the
  lineage (generations, merge, graft), search, minting, the narrator. Where general work lands
  first.
- **[`arc-solver-agent`](https://github.com/IsaiahN/tether/tree/arc-solver-agent)**:
  `general-agent` plus the ARC-AGI-3 interface, the competition build: it
  receives `general-agent` by merge and adds only what ARC needs.
- **[`development`](https://github.com/IsaiahN/tether/tree/development)**: the working branch for
  the competition build, cut from `arc-solver-agent`; refined changes reach `arc-solver-agent` by
  pull request.

Swap the interface, keep the lineage.

## What it is an example of

A **recursively self-improving agent** of a specific, checkable kind. It does not rewrite its
source code. It rewrites its **vocabulary**: the terms it reasons with.

- **It invents only what pays.** A new term enters its library only if stating it, plus what it
  still fails to explain, costs less than the miss it explains (a minimum-description-length
  bargain).
- **The world settles it, not the agent.** A term is kept because the ground, which here is the
  next observation, agrees. Nothing the agent produces about itself counts as evidence.
- **Settled terms become parts.** Each one is an operand the next search composes over, so every
  idea it keeps makes the next one cheaper to find.
- **It knows when it is stuck.** When nothing it holds can close a gap, it says *unreachable with
  what I hold*. It then splits the question, names a new condition, or waits for an import,
  instead of guessing.
- **It budgets its own thinking and weighs its own choices.** A step thinks about as long as
  its recent steps needed, and work it cannot afford is owed, never judged. Each way of acting
  wins only on what it returned before; a held plan or a goal step proposes and acts only if it
  wins; goals that worked before are tried first; and as new terms arrive, the least-used fall
  back to a second search tier, while nothing is deleted.
- **It carries what it learned.** Between runs it writes a lineage of terms *by kind*, never by
  instance, with their evidence. The next life starts from them.
- **It is whitebox.** Each term carries the atoms and bonds it was built from. The ledger says
  why every decision was made, and `gate.py`, which imports nothing from the agent, can fail the
  run.

The loop is one loop for every world, with no branch on problem type:

    PERCEIVE -> ROUTE -> MINT -> ACCEPT -> SETTLE -> PROMOTE -> IMPORT -> REPEAT

**Already in this branch (all on by default):**

- **The try-first hold reads the agent's own record**: a hypothesis counts only its own presses.
- **A bounded re-check**: the background re-check after a level clear is paid from each step's
  budget, cut and resumed, so it can no longer stall a session.
- **Look-ahead**: settled one-press predictions are chained over short sequences of intentions,
  reading only what is on the board.
- **Routines kept in kind form**: a look-ahead sequence that closes its gap is kept as one
  routine, by kind.
- **The thought record**: each library lookup remembers what it tried and what paid, by kind of
  situation, and ranks what paid first.
- **Self-read**: where each game's chain of reasoning stopped is carried, and read at the next
  game's start.
- **The try-first pass**: the try-first sweep gives every untouched kind one touch before it may
  stop, on boards where an action can be aimed at an object.

**What this release adds (every switch on by default):**

- **Condition search**: when a rule keeps missing on part of what it covers, the agent names the
  condition that separates the misses and searches inside it, nested inside a live split too.
- **Strength and forgetting**: a term is settled only where it beat "no change"; a term whose
  bargain no longer pays is crowded out of a slot and kept in the library. As new material
  arrives, the least-used entries fall to a second search tier; nothing is deleted, and the
  kernel (the priors and what was inherited) is never moved down or crowded out.
- **The purse**: a step thinks in its own counted work, up to its level's median demand plus what
  earlier steps saved; work it cannot afford is "unreached at this budget" and owed, never a
  verdict, and a level that keeps running out widens the purse until half its steps finish.
- **The exit contest**: every contested way of acting bids, and the bid is read off the agent's
  own record of what that way returned before; a held plan, a goal step and a look-ahead each
  propose and act only if they win.
- **The recall-first goal proposer**: goals that won or made progress before are tried first,
  then the shelf's other forms, and the whole library's grammar only while the purse allows.
- **The translation table**: three of the agent's own decisions are written as the steps of the
  formula that decided them, and a step the ground keeps refusing is skipped.
- **Doors**: a guess whose way was blocked is set aside, "not reachable right now", and picked
  back up when the world changes or a new effect is known.
- **The needs dial**: making progress and exploring are weighed by how often each has paid when
  it was tried, learned apart under pressure and at ease, so a need used more does not weigh
  more just for being used.
- **Fair test comparisons**: a test that compares two runs starts each one in its own fresh
  process. A process that has already run the agent works faster, so it would think further on
  the same counted budget, and the comparison would measure the process instead of the change.

## A general learner: swap the two layers, keep the mind

The agent reasons in **intents** (what it wants to be true): `ELICIT`, `TOUCH`, `BE_AT`,
`BECOME`, `DISTINGUISH`. Two thin layers connect it to a world, and they are the only parts that
change.

| Layer | File | Its job |
| --- | --- | --- |
| **Input** (the world adapter) | `world.py`'s `Env` contract | Says what is there. An adapter fills ten members: `substrate`, `environment`, `actors`, `currency`, `ground`, `slots`, `atoms`, `transform`, `actions`, `alphabet`. One that cannot fill them fails at construction. |
| **Output** (the interface) | `interface.py` | Turns an intent into whatever actions the world offers, and reports what each one did. Its table of what each action does starts **empty** and fills only by acting. |

So to point the agent at a new domain, you write an adapter and, if the actions differ, an
interface realiser. The reasoning above them does not change. Three worlds already ship:

- `world.py`, a symbolic world;
- `gridworld.py`, a generated grid habitat;
- `arc_world.py` with `arc_percept.py`, ARC-AGI-3.

Anything that can be read as objects with attributes, and acted on with a finite set of actions,
is a candidate: puzzles, games, simulations, lab or control loops.

## Quick start (about 2 minutes)

Python 3.13. `requirements.lock` pins the whole runtime.

    git clone -b general-agent https://github.com/IsaiahN/tether.git
    cd tether
    python -m venv .venv
    # activate .venv; `python` below is the venv's interpreter on any OS
    python -m pip install --no-deps -r requirements.lock

    python -B demo.py                 # ~10 s, offline: the agent learns a small symbolic world
    python -B gate.py runs/demo.jsonl # the independent checker reads the run's ledger

`demo.py` shows the four things that make it trustworthy:

1. a wrong term located by id, step and the residual it answered;
2. a planted bad atom caught by the ground and traced to its entry;
3. abstention on what it cannot reach, with the budget it spent;
4. the false-abstention rate beside the abstention rate.

To play ARC-AGI-3 games, see the
[`arc-solver-agent`](https://github.com/IsaiahN/tether/tree/arc-solver-agent) README.

## What ships, and what does not

- **Ships:** the code, and the library (`library/`): atoms, molecules, relations and grammar.
  This is the agent's inheritance, what it can *say*. It holds no answer to any problem. A
  missing library stops the agent at startup and names each missing file.
- **Does not ship:** anything learned. The agent starts empty of experience. What it learns goes
  to a lineage folder outside the repository. No lineage, learned library or run output is ever
  committed.

## Read next

- [`figures/`](figures/): the 13 figures, the Operators and Symbols tables, and the formula. The
  figures govern; [`docs/FIGURES_TEXT.md`](docs/FIGURES_TEXT.md) is their text, line-numbered.
- [`docs/LIBRARY_VS_COMPOSER.md`](docs/LIBRARY_VS_COMPOSER.md): why the composer, not the library,
  is the thing.
- [`docs/WHAT_THE_AGENT_SEES.md`](docs/WHAT_THE_AGENT_SEES.md): an ARC game from the agent's
  side.
- [`docs/multi_agent/`](docs/multi_agent/): how many instances would share one store (a design;
  nothing implemented).
- [`docs/reviews/`](docs/reviews/): independent reviews of this release, including where it stands
  against the figures and against animal and child cognition.
- [`docs/INDEX.md`](docs/INDEX.md): every mechanism, mapped to the line of code that decides it.

## The checks

From the repository root, one at a time:

    export PYTHONDONTWRITEBYTECODE=1                    # a POSIX shell; Git Bash on Windows
    python -m ruff check .
    python -B tests/test_gate.py
    python -B tests/test_entry.py
    python -B tests/test_gate_ledger.py
    python -B tests/test_arm_modules.py
    python -B conform/arms.py

Each prints its own result line and exits 0 when it passes. `tests/test_gate.py` checks the
checker itself: one planted defect per check, and every defect must be caught.

## How results are judged

Every term is graded by a ground the library cannot move.

- **Nothing scores itself.** Coverage, terms minted and compression achieved are internal to the
  frame, and are not evidence.
- **Priors are inheritance, not answers.** The library holds human priors the agent starts with,
  the way an animal starts with its instincts. None is written for a particular problem.
- **The ablation is a procedure.** Back up the library, verify the backup, wipe it, and re-run
  (`TETHER_LIBRARY_REQUIRED=0`). If a result survives, the agent composed it; if it disappears,
  the library was carrying it.

No result is claimed here. Results are reported where they are measured, with the world and the
switch state they ran under.
