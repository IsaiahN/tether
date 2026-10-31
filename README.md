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

**The agent's code is the same as on `general-agent`.** For what the agent is and how it
reasons, read [that README](https://github.com/IsaiahN/tether/tree/general-agent). What is
particular to ARC is only the adapter and the harness below.

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

- The submission bundle and the notebook's agent class are not built yet. When built, the
  bundle carries only what the agent imports, and `arcengine` comes from the competition's
  wheels.
- Runner items designed and held for the Kaggle step are in `docs/kaggle_export/E9_RUNNER_HELD.txt`.
- The API key is never committed: `.env` is gitignored, and it appears in no commit.

No result is claimed here. Results are reported where they are measured, with the games, the
population and the switch state they ran under.
