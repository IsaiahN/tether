"""The chunk-sequence feeder and the spacing sweep: the agent watches a human replay, in an
order the seat chooses.

SEAT-SIDE. The agent does not import this, exactly as it does not import `arc_holdout`.

WHY IT EXISTS. F183 traced both of the reviewer's unbuilt items to ONE absent artifact. The
spacing sweep needs a spacing parameter on a curriculum builder and there was no curriculum
builder; the pretraining run IS this thing being run, and the version that produced §14's numbers
was never committed. TRAINING_PLAN §14.4 wants all 25 chunkified WITH OFFSET AUGMENTATION and
§14.5 wants them shuffled then annealed -- neither is expressible without something that puts
chunks in an order and plays them.

THE DESIGN IS A TAPE BEHIND THE EXISTING WORLD, NOT A SECOND WORLD. `ArcWorld` already takes a
`wrapper` it calls `reset()`/`step()` on, so a tape that yields replay frames substitutes for the
live game and EVERY perception path stays identical -- same segmentation, same slots, same atoms.
A parallel env would have been a second implementation of the thing under test.

AND THE AGENT DOES NOT ACT HERE, WHICH IS THE POINT. `step()` advances the tape whatever action is
passed, so the agent predicts, is wrong, and mints against a trajectory it did not choose. That is
§13's *pretending to be the agent* from the other side: it EARNS the composition from watching,
and nothing is installed.

SPACING IS THE ONE DIAL, AND IT IS THE REVIEWER'S PRE-REGISTERED LADDER 1/2/4/8/16. Chunks are
shuffled IN BLOCKS OF `spacing`, so s=1 is random-dense -- no game or temporal structure survives
and only shapes that recur everywhere can pay off -- and a large s is coherent-wider. That is
§14.5's annealing in a single parameter, in the plan's own words: *the spacing dial IS this
annealing*. EVERY RUNG SEES THE IDENTICAL FRAME SET and only the order differs, which is what
makes a difference across rungs readable as ordering rather than as content.

THE WITNESS IS THE TRANSFER CLIFF, NEVER THE RISE -- pre-registered 09-18, failure signature named
in advance: a real capability degrades GRADUALLY as spacing widens; a marker-follower holds flat
then drops off a CLIFF at roughly its trained spacing. THE CURVE IS THE FINDING, NOT THE
ENDPOINTS. So the library carries across rungs, the ramp only goes upward, and the per-rung
library state is logged so a later rise is interpretable rather than confounded.

THE LIBRARY SWITCH IS §17.8's AND WAS ALREADY BUILT -- `arc_holdout.play(library=...)`, load
before and save after. Carrying Γ across rungs needed no new mechanism, only the existing one
pointed at a rung loop.

KEY_BOUNDARY: the tape carries FRAMES, which are what the world showed. It never reads the answer
key's compositions or effects -- `rlvr` does that, afterwards, to score. Watching a human play is
not being told the answer; being handed the derivation would be.
"""

from __future__ import annotations

import collections
import json
import random
import shutil
import sys
import tempfile
import time
from pathlib import Path
from typing import Any

import arc_atoms
import arc_holdout
import arc_percept
import arc_predict
import gamma
import ledger
import reverse_engineer
import rlvr
import tether
from arc_world import ArcWorld

sys.dont_write_bytecode = True

# anchor: ARBITRARY BY REQUIREMENT, AND THAT IS THE ANCHOR -- the seed's only job is to make the
# curriculum a condition someone else can restate, so any fixed value serves and no value is
# better than another. Declared once and never searched: a seed picked by trying several is a
# fitted constant wearing a seed's clothes. THE FALSIFIER: if a rung's reading moves when this
# changes, the reading was seed noise and the sweep owes a result across seeds, not one seed.
# A6i, RECORDED WHILE NOTHING IS WRONG because the colliding item is nameable: 1618 was ALSO the
# held-out-selection seed the reviewer WITHDREW on 2026-09-20 with the subset seal. Different
# quantity, same number, and no code reads both. Do not read this as that seed.
SHUFFLE_SEED = 1618


class _Frame:
    """What `ArcWorld` reads off a frame. Replay steps carry the same fields under other names."""

    def __init__(self, step: dict) -> None:
        self.frame = [step["grid"]]
        self.available_actions = step.get("avail") or ()
        # `or 0`, NOT `get("level", 0)`. SEVEN of the 25 replays -- ar25, cd82, lp85, sb26,
        # sc25, tu93, vc33 -- carry `level: null` in EVERY step, so the key EXISTS and the
        # default never applies. `get` handed None straight to `objective()`, which divides by
        # it. dc22 records levels, which is why four single-game rungs passed and the pooled
        # tape died at cycle 15: a defect only a tape spanning games could reach.
        self.levels_completed = step.get("level") or 0
        self.win_levels = 0

    def is_empty(self) -> bool:
        return not self.frame or not self.frame[0]


class ReplayTape:
    """A `wrapper` that plays recorded frames instead of stepping a game."""

    def __init__(self, steps: list[dict], order: list[int]) -> None:
        self._steps = steps
        self._order = order
        self._i = 0

    def reset(self) -> _Frame:
        self._i = 0
        return _Frame(self._steps[self._order[0]])

    def step(self, _action: Any = None, **_data: Any) -> _Frame:
        # the action is IGNORED and that is deliberate -- see the module docstring. `data=` is
        # the positioned click's coordinate; a tape has none to honour, the human's own is
        # already in the recorded frame.
        self._i = min(self._i + 1, len(self._order) - 1)
        return _Frame(self._steps[self._order[self._i]])


def chunk_order(game: str, offset: int = 0, spacing: int = 1, skip: int = 0,
                take: int | None = None,
                seed: int = SHUFFLE_SEED) -> tuple[list[dict], list[int], int]:
    """The frame sequence for one game, cut at `offset` and coherent in blocks of `spacing`.

    Shuffled BY CHUNK, never by frame: a shuffled frame sequence would destroy the within-chunk
    transitions that ARE the thing being learned. `spacing >= len(chunks)` is one block, which is
    the human's own order -- so full coherence is a rung on the same dial, not a separate mode.

    `skip`/`take` cut a window of CONTIGUOUS chunks, and contiguity is not a convenience: a
    strided sample would leave neighbouring chunks non-adjacent in the human's trajectory, so a
    wide-spacing rung would no longer be coherent and the dial would stop meaning what it says.
    The window is the same for every rung, which is what keeps the frame set identical across
    the ladder. Its cost is a declared boundary -- one cut of one game -- and `offset` is the
    existing answer to that, never a claim that the window is representative.
    """
    if spacing < 1:
        raise ValueError(f"spacing is a block length and must be >= 1, not {spacing}")
    steps = reverse_engineer.load_replay(f"replays/{game}_human.ndjson")
    chunks = reverse_engineer.chunk_replay(steps, offset=offset)
    chunks = chunks[skip:] if take is None else chunks[skip:skip + take]
    blocks = [chunks[i:i + spacing] for i in range(0, len(chunks), spacing)]
    random.Random(seed).shuffle(blocks)
    return steps, [i for b in blocks for c in b for i in c["idx"]], len(chunks)


ALL_GAMES = tuple(sorted(
    x.name[:-len("_human.ndjson")] for x in Path("replays").glob("*_human.ndjson")))


def pooled_order(games=ALL_GAMES, offset: int = 0, spacing: int = 1, skip: int = 0,
                 take: int | None = None,
                 seed: int = SHUFFLE_SEED) -> tuple[list[dict], int]:
    """S14.5 PHASE 1: every game's chunks in ONE pool, block-shuffled TOGETHER.

    This is the thing the single-game dial cannot express. Phase 1's point is that *no game or
    temporal structure survives, so only the shapes that recur EVERYWHERE pay off* -- which needs
    chunks from different games adjacent to each other, not one game reordered.

    At `spacing >= chunks-per-game` each game is one block and the shuffle is game-level: S14.6's
    end state, all 25 interleaved as ONE game. So the same dial spans phase 1 to phase 3.

    Returns the frames already in order, each tagged with the game it came from -- the tape needs
    the tag to keep mint provenance right, see `watch_many`) -- AND THE BLOCK COUNT, because the
    dial can be INERT and nothing else shows it. Blocks are cut per game, so at `take=1` every
    game is one chunk and therefore one block WHATEVER `spacing` says: measured, `spacing=1` and
    `spacing=4` give byte-identical tapes at `take=1`. A pooled ladder run that way yields four
    identical rungs, which reads as *the dial has no effect* when it means *the dial was never
    connected*. **A pooled ladder needs `take >= 2`, and `take >= 8` to span 1/2/4/8.**
    """
    blocks = []
    for g in games:
        steps = reverse_engineer.load_replay(f"replays/{g}_human.ndjson")
        chunks = reverse_engineer.chunk_replay(steps, offset=offset)
        chunks = chunks[skip:] if take is None else chunks[skip:skip + take]
        for i in range(0, len(chunks), spacing):
            blocks.append([dict(steps[j], _game=g)
                           for c in chunks[i:i + spacing] for j in c["idx"]])
    random.Random(seed).shuffle(blocks)
    return [f for b in blocks for f in b], len(blocks)


def watch_many(games=ALL_GAMES, cycles: int | None = None, offset: int = 0, spacing: int = 1,
               skip: int = 0, take: int | None = 4, led_path: str | None = None,
               on: str | None = None, store: str | None = None) -> dict:
    """Watch a POOLED tape across games. One library, no game label reaching the agent.

    PROVENANCE IS KEPT BY ROTATING `gamma.game` AS THE TAPE CROSSES GAMES. `Gamma` reads
    `self.game` AT MINT TIME (`term.handle(self.game)`), so a term minted while watching `dc22`
    frames is stamped `dc22` -- which is S13 step 5's *game-of-origin, proctor-only*, and it is
    not reconstructible afterwards. The agent never reads it; only the handle carries it.

    KNOWN OPEN POINT, recorded rather than silently decided: `Gamma.load` marks a term IMPORTED
    when its stored game differs from `self.game`. With a rotating label a RELOADED pooled library
    would mark almost everything imported. Pooled runs therefore do not carry a library file yet;
    resolving that is a ruling about what cross-game means inside one pooled run, not a patch.
    """
    frames, nblocks = pooled_order(games, offset=offset, spacing=spacing, skip=skip, take=take)
    tape = ReplayTape(frames, list(range(len(frames))))
    fr = tape.reset()
    # the palette is READ across the whole pooled tape -- a per-game palette would make the
    # agent's colour alphabet change under it mid-run, which is a habitat change, not a curriculum
    palette = max(int(v) for f in frames for row in f["grid"] for v in row) + 1

    env = ArcWorld(tape, arc_percept.Objects(),
                   arc_atoms.three_spaces(arc_predict.predict()),
                   palette=palette, name="pooled")
    g = gamma.Gamma(env.atoms(), game=frames[0]["_game"])
    base = len(g.library)
    ag = tether.Agent(env, g, tether.Config(), ledger.Ledger(led_path))
    seen_order = []
    for i in range(cycles if cycles is not None else len(frames)):
        g.game = frames[min(i, len(frames) - 1)]["_game"]
        seen_order.append(g.game)
        ag.step()

    # A GROUND READING, OR THIS RUN REPORTS ONLY FRAME-INTERNAL COUNTS. `library 48 -> 101`
    # would have read as success at rung 1 and the probe is what refused it. `on` probes a live
    # board with the pooled library, scored by rlvr's scorer -- same instrument, same baseline,
    # so a pooled result is directly comparable to the ladder's 9/150.
    ground = {}
    if on:
        path = store or str(Path(tempfile.gettempdir()) / "pooled_lib.json")
        g.save(path)
        ground = probe(on, path)
    mints = collections.Counter(h.split("_", 1)[0] for h in g.handles.values())
    return {"games": len(games), "spacing": spacing, "offset": offset,
            "take_per_game": take, "frames": len(frames), "blocks": nblocks,
            "dial_inert": nblocks == len(games),
            "cycles": cycles if cycles is not None else len(frames),
            "palette": palette, "switches": sum(1 for a, b in zip(seen_order, seen_order[1:],
                                                              strict=False) if a != b),
            "atoms": base, "library": len(g.library), "minted": len(g.library) - base,
            "settled": len(g.settled_terms), "by_origin": dict(mints.most_common(8)),
            "fr": fr is not None, **ground}


def watch(game: str = "dc22", cycles: int | None = None, offset: int = 0, spacing: int = 1,
          skip: int = 0, take: int | None = None,
          library: str | None = None, led_path: str | None = None) -> dict:
    """Run the agent over a replay tape. `cycles=None` walks the WHOLE tape exactly once.

    The default is the whole tape because a prefix makes rungs incomparable: 20 cycles of a
    coherent tape is the game's opening and 20 of a shuffled one is a random chunk mid-game --
    a difference in CONTENT wearing a difference in ORDER's clothes.
    """
    steps, seq, n_chunks = chunk_order(game, offset=offset, spacing=spacing,
                                       skip=skip, take=take)
    tape = ReplayTape(steps, seq)
    fr = tape.reset()
    board = fr.frame[-1]
    palette = int(max(int(v) for row in board for v in row)) + 1

    env = ArcWorld(tape, arc_percept.Objects(),
                   arc_atoms.three_spaces(arc_predict.predict()),
                   palette=palette, name=game)
    g = gamma.Gamma(env.atoms(), game=game)
    base = len(g.library)
    if library and Path(library).exists():
        g.load(library)
    carried = len(g.library)
    ag = tether.Agent(env, g, tether.Config(), ledger.Ledger(led_path))
    for _ in range(cycles if cycles is not None else len(seq)):
        ag.step()
    if library:
        g.save(library)

    return {"game": game, "offset": offset, "spacing": spacing,
            "chunks": n_chunks, "blocks": -(-n_chunks // spacing),
            "frames": len(seq), "cycles": cycles if cycles is not None else len(seq),
            "atoms": base, "carried_in": carried - base,
            "library": len(g.library), "minted": len(g.library) - carried,
            "settled": len(g.settled_terms), "promotions": len(g.primitives)}


def probe(game: str, library: str, cycles: int = 25) -> dict:
    """Score a CARRIED library on a live board, with `rlvr`'s scorer and no new metric.

    Against a COPY: `play` saves after the run, so probing the training path would fold probe
    experience back into training and the next rung would inherit it.
    """
    tmp = f"{library}.probe"
    shutil.copyfile(library, tmp)
    seen: list = []

    def tap(was, _action, now):
        if not seen and was is not None:
            seen.append(was)
        if now is not None:
            seen.append(now)

    arc_holdout.play(game=game, cycles=cycles, library=tmp, on_frame=tap)
    # COMPONENTS, NOT BOARDS. `_rate` scores over segmented objects and `against_null` converts
    # before calling it; passing raw boards here read as a plausible call and is a different
    # quantity. Caught by reading the only existing caller rather than the callee's signature.
    objs = [arc_percept.components(b) for b in seen]
    kp = Path(f"replays/{game}_answer_key.json")
    key = (json.loads(kp.read_text(encoding="utf-8")) if kp.exists()
           else reverse_engineer.answer_key(f"replays/{game}_human.ndjson"))
    hit, tot, rows = rlvr._rate(objs, key)
    Path(tmp).unlink(missing_ok=True)

    # DISTINCT EFFECTS, because hit/tot is quantised in lumps and hides what moved. dc22's 150
    # non-trivial chunks carry 120 DISTINCT signatures and the agent matches exactly ONE -- the
    # second-commonest, which covers 9 chunks. So 9/150 is 1/120 by effect, and the probe cannot
    # read anything but 9 until a SECOND signature is acquired. `hit` flat at exactly 9 is
    # therefore not insensitivity: it is "still one signature, still the same one".
    # `_rate` appends one row per NON-TRIVIAL chunk in key order, so the two zip.
    nt = [c for c in key["chunks"]
          if any(c["signature"][k] for k in ("moved", "resized", "recoloured",
                                             "vanished", "appeared"))]
    got = {json.dumps(c["signature"], sort_keys=True)
           for c, r in zip(nt, rows, strict=False) if r["achieved"]}
    allsig = {json.dumps(c["signature"], sort_keys=True) for c in nt}
    return {"probe": game, "hit": hit, "of": tot,
            "pct": round(100 * hit / tot, 1) if tot else 0.0,
            "distinct": len(got), "of_distinct": len(allsig)}


def sweep(game: str = "dc22", rungs=(1, 2, 4, 8, 16), cycles: int | None = None,
          offset: int = 0, skip: int = 0, take: int | None = None,
          on: str | None = None, store: str | None = None,
          led_dir: str | None = None) -> dict:
    """The spacing sweep. PRIORITY 0 -- Isaiah 2026-09-20; pre-registered by the reviewer 09-18.

    RAMP UPWARD ONLY, so a regression is unambiguous. ONE library across every rung, because
    gamma is the agent's only memory and wiping it between rungs is a different experiment
    rather than a cleaner one.
    """
    path = store or str(Path(tempfile.gettempdir()) / f"sweep_{game}_{offset}.json")
    Path(path).unlink(missing_ok=True)
    # EACH RUNG IS WRITTEN AS IT LANDS. A rung costs hours at the measured mint cost, so a
    # sweep that only reports at the end reports nothing at all if it is interrupted -- and a
    # partial ladder is still a curve, which is the witness.
    trail = Path(f"{path}.rungs.ndjson")
    trail.unlink(missing_ok=True)
    rows = []
    for s in sorted(rungs):
        t0 = time.time()
        # A LEDGER PER RUNG, because the summary counts cannot answer the question the
        # reviewer's own conditions turn on -- did PROCEDURE-level reuse fire? `routine_cut` is
        # measured at zero on four boards and the ladder is meant to be what forces it. Without
        # a ledger a rung reports minted/settled and nothing about reuse. Routing an existing
        # recorder to a file, not a new instrument.
        led = f"{led_dir}/rung_{game}_s{s}.jsonl" if led_dir else None
        row = watch(game, cycles=cycles, offset=offset, spacing=s,
                    skip=skip, take=take, library=path, led_path=led)
        row["ledger"] = led
        if on:
            row.update(probe(on, path))
        row["secs"] = round(time.time() - t0, 1)
        rows.append(row)
        with trail.open("a", encoding="utf-8") as fh:
            print(json.dumps(row), file=fh)
    return {"sweep": game, "probe_on": on, "offset": offset,
            "window": {"skip": skip, "take": take}, "rungs": sorted(rungs),
            "carried": path, "trail": str(trail), "rows": rows,
            "reads": ("the witness is the SHAPE across rungs, not any endpoint: gradual "
                      "degradation reads as capability, flat-then-cliff as a marker-follower")}


if __name__ == "__main__":
    # two entry points because there are two curricula: one game's order (the ladder), and all
    # 25 pooled (S14.5 phase 1). Same dial, different tape.
    mode = sys.argv[1] if len(sys.argv) > 1 else "sweep"
    if mode == "pooled":
        n = int(sys.argv[2]) if len(sys.argv) > 2 else 40
        sp = int(sys.argv[3]) if len(sys.argv) > 3 else 1
        tk = int(sys.argv[4]) if len(sys.argv) > 4 else 4
        print(json.dumps(watch_many(cycles=n, spacing=sp, take=tk), indent=1))
    else:
        g = sys.argv[2] if len(sys.argv) > 2 else "dc22"
        n = int(sys.argv[3]) if len(sys.argv) > 3 else 0
        print(json.dumps(sweep(g, cycles=n or None), indent=1))
