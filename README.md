# tether -- the ARC solver agent

Branch `arc-solver-agent`. This branch is the general agent applied to ARC-AGI-3. The agent's
code is the same as on `general-agent`; what is particular to ARC is the world adapter and the
harness that plays games. For what the agent is and how it reasons, read the README on
`general-agent`:

    git clone -b general-agent https://github.com/IsaiahN/tether.git

## How the agent meets ARC

- **The input side** is `arc_world.py` (`ArcWorld`), an adapter filling `world.py`'s `Env`
  contract over the `arc_agi` package. It reads the frame and the wrapper's own surface, and
  nothing that knows what a board means. Objects are found and tracked by `arc_percept.py`.
- **The action side** is `interface.py`, unchanged from `general-agent`: the agent decides an
  intent, and the interface realises it as one of the actions the game offers. The platform's
  RESET is offered like any other action, with one hard rule: never two RESETs in a row.
- **The harness** is `arc_holdout.py` (`play`, `wire`) and the entry point `tether_agent.py`
  (`run`). A game ends on a WIN, the step cap or the time allowance. A game over does not end
  the run: the boundary is marked, play goes on, and the agent may choose to RESET. The entry
  point never presses RESET for it.
- **The agent is told nothing about a game** beyond what it perceives: no goal and no rules. By
  the project's standing rule, no decision may read a game's identity.

## What ships, and what does not

- **Ships:** the code and the library (`library/`), as on `general-agent`.
- **Does not ship:** the learned library. What the agent learns while playing (its lineage: one
  generation file per game, plus its memory store) is written to the `lineage_dir` you give it,
  outside the repository, and is never committed.
- **Not ours to ship:** the games (`environment_files/`), recordings and human replays. All are
  gitignored.

## From a fresh clone

Python 3.13 (`pyproject.toml`: `>=3.13,<3.14`).

    git clone -b arc-solver-agent https://github.com/IsaiahN/tether.git
    cd tether
    python -m venv .venv
    # activate .venv; `python` below is the venv's interpreter on any OS
    python -m pip install --no-deps -r requirements.lock

Fetch a game once with the `arc_agi` package's own anonymous fetch (every run after that is
offline), then play it, carrying a lineage folder (created if absent; give the same folder again
to carry on from it):

    python -c "from arc_agi import Arcade; from arc_agi.base import OperationMode; Arcade(operation_mode=OperationMode.NORMAL).make('<game_id>')"
    python -B -c "import arc_holdout; print(arc_holdout.play('<game_id>', 40, lineage_dir='lineage')['persistence']['lineage'])"

The checks are the same six as on `general-agent`.

## Kaggle notes

- The submission bundle and the notebook's agent class are not built yet (the earlier
  `kaggle_bundle.py` and `kaggle_agent.py` were removed on 2026-10-24). When built, the bundle
  carries only what the agent imports, and `arcengine` comes from the competition's wheels.
- Runner items designed and held for the Kaggle step are in `docs/kaggle_export/E9_RUNNER_HELD.txt`.
- The API key is never committed: `.env` is gitignored, and it appears in no commit.

No result is claimed here. Results are reported where they are measured, with the world, the
population and the arm state they ran under.
