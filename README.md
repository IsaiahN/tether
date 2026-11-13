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

**Already in production (all on by default):**

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
- **The needs dial**: making progress and exploring are weighed by how often each has paid when
  it was tried, learned apart under pressure and at ease, so a need used more does not weigh
  more just for being used.
- **Fair test comparisons**: a test that compares two runs starts each one in its own fresh
  process. A process that has already run the agent works faster, so it would think further on
  the same counted budget, and the comparison would measure the process instead of the change.
- **A general agent or a specialist one** (`TETHER_GENERAL`): on, the general agent can lose
  context: what goes unused is reached for less readily, never deleted. Off, the specialist agent
  still learns new things and never forgets: every fade below is switched off.
- **Fading by disuse**: a habit that once paid is reached for less readily the longer it sits
  unused, and one use brings it back; an old failure is slowly forgiven. What it believes is true
  never fades.
- **A bank per board**: thinking a board saves is spent on that board's harder questions, and a new
  board starts with an empty bank, so one game's savings never carry into the next.
- **The purse inside each unit**: a lookup or a mint that would run past the step's allowance stops
  at its next loop and is owed, and the step still makes and records its choice.
- **Walks shared by pattern**: a library walk worked out for one set of objects is reused for any
  set in the same arrangement, the names substituted, so the same thinking costs less.
- **Time counted by learning** (`TETHER_FADE_BY_STORE`): fading runs on how much the agent has
  written to memory, not on how many steps pass, so a board where nothing new happens ages
  nothing. When something fails again, its earlier failures are re-judged by what kind of thing
  they were, never by name; before there is enough to measure, only steps in which something was
  learned count.
- **One-off sightings fold into their idea** (`TETHER_FOLD`): at a game's end, something seen only
  once is counted on the general idea it belongs to instead of kept as its own record, so memory
  grows with what recurs.
- **Proven and recent first** (`TETHER_RELEVANCE`): among library entries that fit equally well,
  the order is by how well each has held up and how recently it was used, and one never tried gets
  a small head start; fit still comes first, and what the agent believes does not change.
- **A lost game is not repeated by another route**: every way the agent chooses a move now avoids
  a move that lost on this same board before, unless no other move is left.
- **Goal-finding and invention stay inside the budget**: proposing goals and building new
  candidates stop when the step's allowance is spent and are owed, instead of running long.
- **Step 8, a better-ordered search for explanations** (built): the agent indexes where each
  change came from (itself, a neighbour, its own clock, or hidden), skips candidates that already
  failed and rescans only what changed, walks the cheapest fitting ideas first and stops when
  nothing better can come, keeps word senses apart by context, weights its narration, and keeps a
  book of which settled ideas paid where -- each behind its own switch, on by default. Nested
  ideas (an idea's input computed by another idea) are in place but not yet built by the agent.
- **Played offline on five public games** (vc33, tn36, ft09, dc22, bp35, in the arcade's order)
  from its carried library, this build met the rule set before the run: no faults, no game
  finishing fewer levels, no doubling of empty lookups, and no game losing its goal-directed moves
  (ft09 kept its one and reached it sooner; vc33 gained two). It took fewer steps in the same time
  on all five games, most on tn36 and bp35; that cost is being profiled for the next release.
- **The repository is reorganized**: docs/ in numbered folders with a README in each, and run
  logs written to logs/.

**The agent's code is `general-agent`'s plus the build above;** once today's `general-agent`
pull request merges, the agent's code is the same on both, and this branch adds only the ARC
adapter, the harness and the Kaggle runner. For what the agent is
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

## Documents

The documents are in numbered folders under `docs/`; start at
[docs/00-README.md](docs/00-README.md). Each folder has its own README.

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
