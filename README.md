# tether — the ARC-AGI-3 solver agent

The [general tether agent](https://github.com/IsaiahN/tether/tree/general-agent), pointed at
[ARC-AGI-3](https://arcprize.org/): interactive games it has never seen, with no instructions,
no stated goal and no rules. It has to find out what the game is by playing it, as a person
would.

It is built on **The Tether** architecture:

- *Arrival of the Fittest: The Tether Architecture*:
  [Medium](https://medium.com/@IsaiahNwukor/arrival-of-the-fittest-the-tether-architecture-1de7edf641ec)
  · [Substack](https://adventuresinml.substack.com/p/arrival-of-the-fittest-the-tether)
- The figures and the formula are in [`figures/`](figures/).

## The four branches

- **[`core`](https://github.com/IsaiahN/tether/tree/core)**: the minimal kernel. The Tether loop,
  gate and abstention on a toy symbolic world, about 1,600 lines. Read this first to see the
  architecture whole.
- **[`general-agent`](https://github.com/IsaiahN/tether/tree/general-agent)**: the full general
  learning agent. Domain-agnostic: the library of ~4,000 human-prior entries, the lineage
  (generations, merge, graft), search, minting, the narrator. Where general work lands first.
- **[`arc-solver-agent`](https://github.com/IsaiahN/tether/tree/arc-solver-agent)** (this one):
  production.
  `general-agent` plus the ARC-AGI-3 interface and the Kaggle runner. The competition build, and
  what a Kaggle submission is built from: it receives `general-agent` by merge and adds only what
  ARC needs. It changes only by a pull request from `development`.
- **[`development`](https://github.com/IsaiahN/tether/tree/development)**: the working branch,
  promoted to arc-solver-agent by pull request once its changes are refined. A test bundle built
  from it is labelled DEV.

Swap the interface, keep the lineage.

**What this production carries, promoted from `development` (all on by default):**

- **Strength and forgetting**: a term is tipped to settled only where it beat "no change"; a
  term whose bargain no longer pays against the null is crowded out of a slot and kept in the
  library; a miss is cut by the condition that separates it (nested inside a live split, too).
  What is reachable falls into a second tier when new material arrives; nothing is deleted, and
  the kernel (the priors, what was inherited) is never moved down or crowded out.
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
  back up when the board moves or a new effect is known.
- **The needs dial**: making progress and exploring are weighed by how often each paid when it
  was chosen, learned apart under pressure and at ease, so a need used more does not weigh more
  just for being used.
- **Fair test comparisons**: a test that compares two runs starts each one in its own fresh
  process. A process that has already run the agent works faster, so it would think further on
  the same counted budget, and the comparison would measure the process instead of the change.

**The agent's code is `general-agent`'s plus FIN5E and the build above.** For what the agent is
and how it reasons, read [that README](https://github.com/IsaiahN/tether/tree/general-agent). What is particular to
ARC is only the adapter and the harness below.

## How it meets an ARC game

- **It sees the frame, and nothing that says what it means.** `arc_world.py` (`ArcWorld`) fills
  the general `Env` contract over the `arc_agi` package. `arc_percept.py` finds and tracks
  objects: every same-colour region, read exactly, with position, size, shape, colour, the
  changes in each, and contact between objects.
- **It acts through the same interface.** `interface.py` turns the agent's intents into the
  game's actions: the directional actions, the one positioned click, and RESET. RESET is
  offered like any other action, with one hard rule: never two RESETs in a row.
- **It forms its own goals.** It is never told a game's name, goal or rules, and no decision may
  read a game's identity. It proposes candidate goals from its own condition grammar over the
  board in front of it, chases them, and keeps what held when a level clears.
- **It learns across games.** What it learns goes to a lineage folder you name: one generation
  per game, plus its memory store, carried by kind, never by game. Give the same folder again to
  carry on from it.
- **The harness** is `arc_holdout.py` (`play`, `wire`), with the entry point `tether_agent.py`
  (`run`). A game ends on a WIN, the step cap or the time allowance. A game over does not end
  the run: play goes on, and the agent may choose to RESET. The entry point never presses RESET
  for it.

## Quick start

Python 3.13. `requirements.lock` pins the whole runtime.

    git clone -b arc-solver-agent https://github.com/IsaiahN/tether.git
    cd tether
    python -m venv .venv
    # activate .venv; `python` below is the venv's interpreter on any OS
    python -m pip install --no-deps -r requirements.lock

Fetch a game once with the `arc_agi` package's own anonymous fetch (every run after that is
offline), then play it with a lineage folder (created if absent):

    python -c "from arc_agi import Arcade; from arc_agi.base import OperationMode; Arcade(operation_mode=OperationMode.NORMAL).make('<game_id>')"
    python -B -c "import arc_holdout; print(arc_holdout.play('<game_id>', 40, lineage_dir='lineage')['persistence']['lineage'])"

To see the agent learn offline first, with no game needed, run `python -B demo.py`; see the
[general README](https://github.com/IsaiahN/tether/tree/general-agent).

The checks are the same six as on `general-agent`.

## What ships, and what does not

- **Ships:** the code and the library (`library/`), as on `general-agent`.
- **Does not ship:** the learned library. What the agent learns while playing is written to the
  `lineage_dir` you give it, outside the repository, and is never committed.
- **Not ours to ship:** the games (`environment_files/`), recordings and human replays. All are
  gitignored.

## Kaggle notes

- `kaggle/` holds the submission. `make_notebook.py` renders `tether_a.ipynb`, which plays the
  games the competition's gateway lists, in its order, as one life that carries one lineage,
  and `probe_machine.ipynb`, which prints the machine's cores, memory, disk and Python.
- `build_dataset.py` and `build_lineage.py` build the two Kaggle datasets: the code with the
  library, and the learned lineage, each with a sha256 manifest. The lineage is never in this
  repository.
- The notebook installs offline from the competition's own wheelhouse; `arcengine` comes from
  those wheels.
- The API key is never committed: `.env` is gitignored, and it appears in no commit.

No result is claimed here. Results are reported where they are measured, with the games, the
population and the switch state they ran under.
