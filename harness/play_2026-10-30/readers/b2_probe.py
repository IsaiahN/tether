"""r424 B2: ONE cold agent carried through a fixed order of games, N steps each, the way e4_stream carries it (one
proxy wrapper, the next game made current between steps and its first frame handed over by env.arrive(), retarget on
a terminal edge as the stream does; no lineage, no game id passed). Each game is profiled on its own (cProfile only
around step_or_recover), and the ledger is written, so the repeat rows' wall_s give PERCEIVE per step per game.
Writes <out>/stream.jsonl, <out>/<i>_<game>.pstats, <out>/b2.json. argv: tree out steps game[,game...]"""
import cProfile
import json
import logging
import os
import sys
import time

sys.dont_write_bytecode = True
tree, out, n, order = sys.argv[1], sys.argv[2], int(sys.argv[3]), sys.argv[4].split(",")
# B3 (r426): an item may carry its own step count as game:steps; a game may repeat, so outputs are keyed by index
plan = [(x.split(":")[0], int(x.split(":")[1]) if ":" in x else n) for x in order]
order = [g for g, _s in plan]
assert os.environ.get("PYTHONHASHSEED") == "0" and os.environ.get("TETHER_AGENT_SEED") == "0"
assert not any(k.startswith("TETHER_") and k not in ("TETHER_AGENT_SEED", "TETHER_ARRIVAL_ALIAS")
               for k in os.environ), "a TETHER_ arm is set"   # r434's OFF twin sets only the alias arm
os.makedirs(out, exist_ok=True)
sys.path = [p for p in sys.path if "scratchpad" not in p.replace("\\", "/")]
sys.path.insert(0, tree)
os.chdir(tree)
logging.disable(logging.INFO)
import arc_holdout  # noqa: E402
import ledger  # noqa: E402
import tether  # noqa: E402
from arc_agi import Arcade  # noqa: E402


class Stream:
    """e4_stream's proxy, switch 'between' only."""

    def __init__(self, arc, first):
        self.arc, self.cur = arc, arc.make(first)

    @property
    def observation_space(self):
        return getattr(self.cur, "observation_space", None)

    def reset(self):
        return self.cur.reset()

    def step(self, act, data=None):
        return self.cur.step(act, data=data) if data is not None else self.cur.step(act)

    def switch_to(self, game):
        self.cur = self.arc.make(game)


arc = Arcade(operation_mode=arc_holdout._mode())
proxy = Stream(arc, order[0])
led_path = os.path.join(out, "stream.jsonl")
env, ag, led, _board, _pal, _loaded = arc_holdout.wire(proxy, "stream", led_path=led_path, lineage_dir=None)
ctx = {"game": "stream", "cfg": None, "library": None, "lineage_dir": None, "led_path": led_path,
       "save_only_dir": None, "palette": _pal}
rec = {"tree": tree, "order": order, "steps": n, "library": len(ag.gamma.library), "games": []}
RT = {"n": 0}
_rt = ag.retarget


def _count_retarget(*a, **k):
    RT["n"] += 1
    return _rt(*a, **k)


ag.retarget = _count_retarget


def held():
    """r426's boundary read: the trace, its window, the bindings, and retargets so far."""
    board = {str(s).split(".", 1)[0] for s in (getattr(ag, "slots", None) or ())}
    out_ = getattr(ag, "_outstanding", {}) or {}
    tried = getattr(getattr(ag, "agency", None), "tried", {}) or {}
    return {"trace": len(getattr(ag, "trace", ())), "window_at": getattr(ag, "_window_at", None),
            "bound": len(getattr(ag, "bound", ()) or ()), "retargets": RT["n"],
            # r427 / r429: the per-play containers' sizes and how much of each names this board
            "board_objects": len(board),
            "outstanding": len(out_), "outstanding_on_board": sum(
                1 for s in out_ if str(s).split(".", 1)[0] in board),
            "tried": len(tried), "tried_on_board": sum(
                1 for s, _a in tried if str(s).split(".", 1)[0] in board)}


T0 = time.time()
for i, (g, gn) in enumerate(plan):
    at_switch = held()
    if i:
        proxy.switch_to(g)
        assert env.arrive(), ("arrive: no frame", g)
    pr = cProfile.Profile()
    c0, walls, was_terminal, lv_seen = ag.cycle, [], "", 0
    steps_rec: list = []
    for _ in range(gn):
        t0 = time.time()
        pr.enable()
        env, ag, acted, fault = arc_holdout.step_or_recover(env, ag, ctx)
        pr.disable()
        walls.append(round(time.time() - t0, 2))
        _ag = ag.agency                         # r434: Agency's reading and integer totals per step
        steps_rec.append({"cycle": ag.cycle, "contingent": len(_ag.contingent()), "mode": _ag.mode(),
                          "tried_sum": sum(_ag.tried.values()), "moved_sum": sum(_ag.moved.values()),
                          "dormant_tried_sum": sum(getattr(_ag, "dormant_tried", {}).values()),
                          "dormant_moved_sum": sum(getattr(_ag, "dormant_moved", {}).values())})
        if fault is not None:
            raise fault
        lv = env.levels()[0]
        end = env.terminal()
        if end and end != was_terminal:
            ag.retarget(env, lv, how=end)
        if tether._LINEAGE_HOLD and was_terminal == "death" and not end:
            ag.restarted(env)
        if not (end and end != was_terminal) and lv > lv_seen and tether._LEVEL_EDGE:
            ag.retarget(env, lv, how=ledger.ADVANCE)
        lv_seen, was_terminal = lv, end
        if end == ledger.WIN:
            break
    pr.dump_stats(os.path.join(out, f"{i}_{g}.pstats"))
    rec["games"].append({"i": i, "game": g, "cycle_start": c0, "cycle_end": ag.cycle, "step_wall_s": walls,
                         "held_before_switch": at_switch, "held_at_end": held(), "steps": steps_rec})
    print(i, g, "cycles", c0, "->", ag.cycle, "walls", walls, "held", held(), flush=True)
ag.end_run("cap")
close = getattr(ag.led, "close", None)
if close:
    close()
rec["wall_s"] = round(time.time() - T0, 1)
with open(os.path.join(out, "b2.json"), "w", encoding="utf-8") as fh:
    json.dump(rec, fh, indent=1)
print("DONE", rec["wall_s"], flush=True)
