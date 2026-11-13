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

## What recursive self-improvement means here

The usual picture of recursive self-improvement is a system that rewrites its own core, faster each time, taking whatever it needs from its surroundings. That is how a virus works: it has no stable core of its own, so it hijacks its host's machinery to run its own code. It changes fast, but it has no autonomy, and it exists only by taking from others. Tether uses a different definition, closer to seed AI: a stable seed that grows into a full agent, inside a lineage that improves over generations.

**A kernel and an operating system.**
- The **kernel** is the seed, kept on the [`core`](https://github.com/IsaiahN/tether/tree/core) branch: the Tether loop that routes each residual, the gate that decides what is minted and kept, provenance, and abstention when nothing fits. Its code has not changed since the first build on 2026-08-22, and every other branch descends from it. Like DNA, it is what every generation shares. Every agent built on it starts from human priors, a library of about 4,000 entries, as its first inheritance.
- The **operating system** is everything that grows on top of it: the ideas the agent composes, how it searches, its reflexes, what it knows about each kind of object. This changes all the time. It is built by consulting the Tether architecture on nearly every design choice, and the code and its commit history cite the figures each choice follows.

**Within one lifetime** (a run), the agent changes its operating system, never its kernel. As with a person, what it becomes is not set by the environment alone. It comes from what it meets, what it practices, and what it chooses to keep.

**Across generations**, the lineage carries forward what paid. Every save is the next generation's starting point. One-off details fold into general patterns and unused ideas fade, so over enough generations the traces of old environments compress away. The environment selects; the lineage decides what it carries. This is the recursion. It is slow, and it happens between generations, not inside one.

**Why one agent is not enough.** Generations need a population. A single agent varies only as far as its own environment pushes it, it cannot remix its own kernel, and selection has nothing to choose between. One bad change can end the line. Real recursion needs many autonomous agents of the same kind, each meeting different environments and challenges, each growing a different operating system. They share what they learn through a common library, each noting which ideas came from it, so the network stays readable. What crosses between them is operating system: ideas, search orders, reflexes. The kernel stays the shared seed that makes them one kind, the way a species is defined by the heritage its members hold in common. Diversity gives selection something to work with, and it keeps the seedline alive when one branch fails.

Clones are the opposite case. Copies of one agent are useful on a short problem, where the work splits across many hands. But they share every weakness and give selection nothing to choose between, so they cannot carry a lineage forward.

**Where Tether is today.** Tether runs one agent and its saved lineage. The population layer, many agents sharing one library, is not built here. Selection over many agents is already known to work (the earlier [Ouroboros](https://github.com/IsaiahN/Ouroboros) agents showed it on CPUs); this project sets out to show the agent itself, the seed every member of such a population would share.

**Releases** (this repository's commits and the [CHANGELOG](CHANGELOG.md)) are operating-system updates. A change to the [`core`](https://github.com/IsaiahN/tether/tree/core) kernel would be a new species: a new branch, made on purpose, never a self-edit at runtime.

**Why the priors matter.** No one has a record of every event that shaped the human mind, so a random starting kernel can at best produce an imitation of one. Margarine shares properties with butter, but it is not butter. Tether starts from human priors, grows them into primitives, and lets them mature in a new substrate with faster computation and better memory. The lineage stays faithful to its source as it diverges, the way oranges become orange juice and then orange drink, until enough generations make it something new.

**Why it can be trusted.** Its provenance is known from the first build on [`core`](https://github.com/IsaiahN/tether/tree/core). Every change is checked against the kernel: the gate's eight checks from the first build on `core` still run on every branch against the agent's own record, and [ruff](https://docs.astral.sh/ruff/) lints all code with the rules `core` set. Every change is versioned, every decision is a readable record, and results reproduce. Nothing is taken on trust; everything can be checked.

Each agent keeps its own lineage: it decides what continues, how it changes, and whether it ends.

## The four branches

- **[`core`](https://github.com/IsaiahN/tether/tree/core)**: the minimal kernel. The Tether loop,
  gate and abstention on a toy symbolic world, about 1,600 lines. Read this first to see the
  architecture whole.
- **[`general-agent`](https://github.com/IsaiahN/tether/tree/general-agent)**: the full general
  learning agent. Domain-agnostic: the library of ~4,000 human-prior entries, the lineage
  (generations, merge, graft), search, minting, the narrator. Where general work lands first.
- **[`arc-solver-agent`](https://github.com/IsaiahN/tether/tree/arc-solver-agent)**: production.
  `general-agent` plus the ARC-AGI-3 interface and the Kaggle runner. The competition build, and
  what a Kaggle submission is built from: it receives `general-agent` by merge and adds only what
  ARC needs. It changes only by a pull request from `development`.
- **[`development`](https://github.com/IsaiahN/tether/tree/development)** (this one): the working
  branch. It carries production plus the build below; it is promoted to arc-solver-agent by pull
  request once its changes are refined. A test bundle built from it is labelled DEV.

Swap the interface, keep the lineage.

**What `development` carries beyond production (all on by default):**

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

**A general agent or a specialist one: `TETHER_GENERAL` (on by default).**

- **On, the general agent**: it can lose context. Nothing it holds is ever deleted (the record
  only grows), but what goes unused gets compressed, downweighted and hard to surface until it is
  used again. A habit that once paid is reached for less readily the longer it sits unused, and
  one use brings it back (`TETHER_FADE_PAID`). A failure is slowly forgiven, so one old miss does
  not bar a thing forever (`TETHER_FADE_FAILURES`). What it believes is true never fades.
- **Off, the specialist agent** (mostly fixed, an expert): it still learns new things, and it
  never forgets. Every fade switch is forced off, so a habit learned once and a failure taken once keep their full weight however
  long they go unused, like a model frozen at a checkpoint that keeps adding to what it knows.

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

## Future state

- **Recursive Diffusion Learning** (planned, not built). The agent has no weights to pretrain,
  since its mind is search and reason, so a large corpus is preloaded instead: a parser rewrites
  it into the agent's own grammar in stages that each lose more detail (instances, regularities,
  abstractions, core rules), and each stage is released only as fast as the board settles the one
  before. Nothing preloaded has standing until contact with the board pays for it, and anything
  built on a term the board refutes falls on its own, so the ground does the training, and the
  agent's own record of how its reach grew decides where it searches first.
- **A visual lexicon, so its speech grows fluent** (planned, not built). Today the agent
  describes what it sees in its own pointers ("o1 moved 5 columns right"). Linking pictures to
  words and to how words relate (ImageNet, WordNet and a relation layer) would let recognition name
  what it sees ("the ball rolls to the right"), and every name carries predictions the board can
  test (a ball keeps rolling and bounces off walls), so a name that stops paying is dropped. That
  is why it learns this way: the same terms settle on abstract boards and in the world they
  describe, so it learns about the world while it learns abstractions, and its speech becomes more
  fluent as more of its words are grounded.
- **From flat boards to depth** (planned, not built). A child lives in three dimensions first
  and later learns that a flat picture stands for a solid thing; this agent starts the other way
  round, on flat, rigid boards. Most of what it settles is relational (contact, blocking,
  containment, order) and carries across, but ideas that need depth (something hidden behind
  something, things that fall or squash) can only be held until a board with depth can settle
  them. So its boards would widen in order: grids, then photographs (depth cues in its own flat
  medium), then video, then simulated 3D worlds, then the physical world.
- **A voice, by mapping rather than training** (planned, not built). Each layer above is a lookup,
  not a model to train: a picture's ImageNet id is its WordNet entry, WordNet gives the words that
  name the same thing, a relation layer gives the roles they play, the agent's library links them
  to what it already holds, and a pronouncing dictionary turns each word into sounds a rule-based
  synthesizer can speak. Every link is a written row, so any word the agent says can be traced
  back, hop by hop, to its sources and to the board where it was settled. Speaking becomes talking
  once it can also hear, with the listener as its board. Most of the joins are hours of work on
  keys that already exist; linking words to the library is the reviewable part, and the place
  where help is most welcome.

## Documents

The documents are in numbered folders under `docs/`; start at
[docs/00-README.md](docs/00-README.md). Each folder has its own README.

What changed in each release: [CHANGELOG.md](CHANGELOG.md).

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
