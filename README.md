# tether — a general learning agent

A CPU-only agent that **teaches itself**. It is given no model of any world and no answers. It
watches, predicts, acts, and keeps only the ideas that the world pays for. The ideas it keeps are
small programs in a typed language, so it builds its own vocabulary and then builds on it. Every
step is written to a record that a separate checker can fail.

It is an instance of **The Tether**, a framework for how intelligence grows by mapping a world
against a ground it cannot argue with.

- *Arrival of the Fittest: The Tether Architecture*:
  [Medium](https://medium.com/@IsaiahNwukor/arrival-of-the-fittest-the-tether-architecture-1de7edf641ec)
  · [Substack](https://adventuresinml.substack.com/p/arrival-of-the-fittest-the-tether)
- The figures it is built from are in [`figures/`](figures/), with the formula,
  [`figures/THE_FORMULA.md`](figures/THE_FORMULA.md).

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
source code. It rewrites its **vocabulary**: the terms it reasons with. Neither do people: no one
rewrites their DNA in a lifetime, yet over years they can become a different kind of person. The
agent can likewise stay general, or lock in what it has learned and specialize, and keep evolving
along that path.

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

The loop is one loop for every world, with no branch on problem type:

    PERCEIVE -> ROUTE -> MINT -> ACCEPT -> SETTLE -> PROMOTE -> IMPORT -> REPEAT

## What it is built to be capable of

These are the capabilities a recursively self-improving, general agent needs, and how this one is
built to meet each. They are design commitments, not results; results are reported where they are
measured.

- **Learn a new task from contact alone.** No instructions, no stated goal, no rules. It finds out
  what a world is by acting in it.
- **Set its own goals.** It proposes candidate goals from its own grammar over what it sees, chases
  them, and keeps what held.
- **Understand cause, not just correlation.** It learns what each action does to what, and keeps a
  prediction only where it beat "no change".
- **Abstract and compose.** It builds new ideas out of settled ones, and relates new things to the
  kinds it already knows.
- **Plan.** It chains settled predictions into short sequences, and a held plan acts only when it
  outbids every other way of acting.
- **Work in any world.** One loop for every world, with no branch on problem type. Swap the
  interface, keep the lineage.
- **Improve itself, recursively.** What it learns becomes what it learns with: a settled term is a
  part the next search builds on, so every idea it keeps makes the next one cheaper.
- **Improve how it improves.** Its thinking budget, its forgetting rate and the weight it gives
  each need are learned from its own record. The loop itself is fixed by design, as evolution's
  is; what changes is everything the loop builds and how it spends.
- **Keep learning for a lifetime without forgetting.** New knowledge is appended, not retrained
  (see below).
- **Transfer.** It carries methods between worlds by kind, never by instance.
- **Know what it does not know.** When nothing it holds can close a gap, it says *unreachable with
  what I hold*, then splits the question or waits for an import, instead of guessing.
- **Stay correctable.** It is graded by a ground it cannot move. Nothing it says about itself
  counts as evidence.
- **Show its work.** It is whitebox (see below).
- **Think within a budget.** Thinking is priced and counted, and work it cannot afford is owed, not
  judged. It runs on a CPU.
- **Grow without a ceiling set by size.** The same loop and rules hold at any scale, the record
  only grows, and what it learns carries forward across lifetimes.

## It learns by appending, not retraining

New knowledge enters as new terms beside the old ones. A term that turns out wrong gets a refusal
added next to it; nothing is rewritten or torn out. What the agent can reach is recomputed from
everything it holds, so a correction in one corner reaches only what was built on that corner.

A neural network updates by retraining its weights, and new training can overwrite old skills
(catastrophic forgetting), so its knowledge tends to be refreshed in whole new versions. Here the
agent keeps its shape and its history while its picture of the world updates one term at a time.
Its starting priors are human knowledge from one point in time; they are a head start it can grow
past, not a fixed snapshot.

## It is whitebox

There are no weights to probe. Every term the agent holds carries the atoms and bonds it was built
from and where it came from. The ledger records why every decision was made. `gate.py`, which
imports nothing from the agent, can fail any run. To see what the agent knows and why, read it
term by term.

## Multi-agent systems, and what "general" means here

**At minimum, a multi-agent system needs a shared channel every agent can both read and write.**
For this agent, that channel would be the library itself:

- traits the agents share are marked as common;
- each agent keeps its own modifications on top, the way an instance inherits from a class;
- every agent can read everyone's combined learning (what to do and what not to do) on similar
  tasks. In a mixture-of-experts setup, agents working on different tasks can correlate what they
  learned in the same store and find the links between them;
- each agent still marks which thoughts and concepts originated with it, so the lineage of every
  idea stays whitebox across the whole network of agents, not only inside one.

This shared library is a design; it is not built in this branch.

**What many agents add is parallelism and scale.** If the agents are selected on, the population
becomes an evolutionary layer, and the best answers surface on their own. This agent leaves that
layer out on purpose: it has been done before, and it is not what this project sets out to show.
Exhibit A is the earlier [Ouroboros](https://github.com/IsaiahN/Ouroboros) agents (v1-v4), which
showed selection over a population works on CPUs; well-known evolutionary algorithms show it too.
Swarms are not new technology. They are selection itself, applied by numbers. Dividing and
conquering by count, like gradient descent, is a strong method, but it is a way to avoid steering
which answers win, not general intelligence.

**A general agent, here, is one that can become anything.** It can stay general, flexible and
changing in proportion to what it meets over time. Or it can choose to lock in what it has learned
and become a specialist in one thing.

**The Tether is the generative code underneath, and it is what makes this possible.** With the
generator, an answer can be generated rather than computed by brute force.

## Language

The agent speaks. Its library is written in a small grammar of universal word meanings (the
primes of the Natural Semantic Metalanguage), and it can say any term it holds, or any decision in
its record, as a sentence in that grammar. Each sentence cites the record row it came from
(`nsm.py`). It can also read a sentence back into a term: every sentence compiles back to the same
term or is refused with a stated reason. It is not as fluent as a language model, but what it says
is tied to what it did and why.

Conversation needs one more thing: a channel that carries other agents' or people's words in and
the agent's sentences out. That is a choice of interface, not an ability the agent lacks. This
general interface provides only the inputs its test worlds give, so it has no such channel yet;
adding one means adding that channel to the interface.

Learning words from outside sources is the same task as reading any arrangement: find what
reliably goes with what, and let meaning come from proximity. The design for this is written:
each kind is organized as a thesaurus of sense clusters, so that "minus" in a ledger and "minus"
on a board are linked but separate. It is not built in this branch.

## Already in this branch (all on by default)

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

## What this release adds (every switch on by default)

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

## Documents

The documents are in numbered folders under `docs/`; start at
[docs/00-README.md](docs/00-README.md). Each folder has its own README.

What changed in each release: [CHANGELOG.md](CHANGELOG.md).

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
