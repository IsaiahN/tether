"""(B), in-game recovery after an agent fault: arc_holdout (wire split, fault key, the helper, the
play call site), tether (the switch), gate (the rule), e4_stream (its call site). argv: tree root."""
import sys
from pathlib import Path

sys.dont_write_bytecode = True
root = Path(sys.argv[1])


def edit(rel, pairs):
    p = root / rel
    s = p.read_text(encoding="utf-8")
    crlf = "\r\n" in s
    s = s.replace("\r\n", "\n")
    for a, b in pairs:
        assert s.count(a) == 1, (rel, a[:80], s.count(a))
        s = s.replace(a, b)
    if crlf:
        s = s.replace("\n", "\r\n")
    p.write_bytes(s.encode("utf-8"))
    print("ok", rel)


# ---------------------------------------------------------------- tether: the CHECK switch
edit("tether.py", [(
    '_ERROR_CARRY = armflag.arm("TETHER_ERROR_CARRY", default=True)\n',
    '_ERROR_CARRY = armflag.arm("TETHER_ERROR_CARRY", default=True)\n'
    '# (B): after an agent fault the same game goes on with a fresh agent loaded from the checked\n'
    '# save (arc_holdout.step_or_recover); OFF, the fault ends the game as item 4 alone does\n'
    '_FAULT_RECOVER = armflag.arm("TETHER_FAULT_RECOVER", default=True)\n')])

# ---------------------------------------------------------------- arc_holdout
A_WIRE_ENV_OLD = '''    env = ArcWorld(w, arc_percept.Objects(),
                   gamma.primitives_once(arc_atoms.three_spaces(arc_predict.predict())),
                   palette=palette, name=game)
    env.on_frame = on_frame     # seat-side tap for §13 step 4's verifier; None on a normal run
    led = ledger.Ledger(led_path)  # a path streams every row to jsonl as it is recorded
'''
A_WIRE_ENV_NEW = '''    env = world_on(w, game, palette, on_frame)
    led = ledger.Ledger(led_path)  # a path streams every row to jsonl as it is recorded
    ag, loaded = wire_agent(env, game, cfg, led, library, lineage_dir)
    return env, ag, led, board, palette, loaded


def world_on(w, game: str, palette: int, on_frame=None):
    """wire()'s world half. (B) builds a fresh one on the SAME ResetGuard-wrapped wrapper: ArcWorld's
    constructor takes the wrapper's observation_space, so a live wrapper is never reset by it."""
    env = ArcWorld(w, arc_percept.Objects(),
                   gamma.primitives_once(arc_atoms.three_spaces(arc_predict.predict())),
                   palette=palette, name=game)
    env.on_frame = on_frame     # seat-side tap for §13 step 4's verifier; None on a normal run
    return env


def wire_agent(env, game: str, cfg: Any, led, library: str | None, lineage_dir: str | None,
               clock: tuple | None = None):
    """wire()'s agent half: the agent on a world and a ledger, its library or lineage load and the
    game-start consolidation. (B)'s fresh agent is built here on the SAME ledger object (wire()
    opens a new Ledger, which truncates its file), with the harness's clock (cycle, deadline) set
    before its load writes a row."""
'''
A_AGENT_OLD = '''    ag = tether.Agent(env, gamma.Gamma(env.atoms(), game=game), cfg, led)
'''
A_AGENT_NEW = '''    ag = tether.Agent(env, gamma.Gamma(env.atoms(), game=game), cfg, led)
    if clock is not None:
        ag.cycle, ag.deadline = clock
'''
A_WIRE_TAIL_OLD = '''        ag._consolidate("game_start")
    return env, ag, led, board, palette, loaded
'''
A_WIRE_TAIL_NEW = '''        ag._consolidate("game_start")
    return ag, loaded
'''
A_NOTE_OLD = '''def note_fault(ag: Any, e: BaseException, led_path: str | None) -> bool:
    """Item 4: an Exception from ag.step(). False when a frame lies inside the game's own packages
    (not the agent's fault: re-raised as before). Else one "@run" "agent_fault" row (type,
    message, the innermost repo frame, the cycle), the whole traceback beside the ledger, and the
    agent marked with the faulted cycle, which its generation leaves out ((C3), lineage._write)."""
    import traceback
    frames = traceback.extract_tb(e.__traceback__)
    if any(any(f"{os.sep}{pk}{os.sep}" in f.filename or f"/{pk}/" in f.filename
               for pk in GAME_PACKAGES) for f in frames):
        return False
    root = os.path.dirname(os.path.abspath(__file__))
    mine = [f for f in frames if os.path.abspath(f.filename).startswith(root)]
    site = f"{os.path.relpath(mine[-1].filename, root)}:{mine[-1].lineno}" if mine else None
    k = len(getattr(ag, "_faults", ())) + 1
    tb_path = f"{led_path}.fault{k}.txt" if led_path else None
'''
A_NOTE_NEW = '''def fault_site(e: BaseException) -> tuple[bool, str | None]:
    """(in the game's own packages, the innermost repo frame as file:line) of an exception."""
    import traceback
    frames = traceback.extract_tb(e.__traceback__)
    if any(any(f"{os.sep}{pk}{os.sep}" in f.filename or f"/{pk}/" in f.filename
               for pk in GAME_PACKAGES) for f in frames):
        return True, None
    root = os.path.dirname(os.path.abspath(__file__))
    mine = [f for f in frames if os.path.abspath(f.filename).startswith(root)]
    return False, (f"{os.path.relpath(mine[-1].filename, root)}:{mine[-1].lineno}" if mine else None)


def fault_key(e: BaseException) -> tuple:
    """(B)'s repeat key: the type and the innermost repo frame; a MemoryError by its type alone,
    since its frame moves with whatever allocated last (the reviewer 2026-10-22 15:17, (C4))."""
    if isinstance(e, MemoryError):
        return (type(e).__name__,)
    return (type(e).__name__, fault_site(e)[1])


def note_fault(ag: Any, e: BaseException, led_path: str | None, k: int | None = None,
               repeat: bool | None = None) -> bool:
    """Item 4: an Exception from ag.step(). False when a frame lies inside the game's own packages
    (not the agent's fault: re-raised as before). Else one "@run" "agent_fault" row (type,
    message, the innermost repo frame, the cycle), the whole traceback beside the ledger, and the
    agent marked with the faulted cycle, which its generation leaves out ((C3), lineage._write).
    (B) passes k, the fault's number in this game, and repeat."""
    import traceback
    in_game, site = fault_site(e)
    if in_game:
        return False
    k = k if k is not None else len(getattr(ag, "_faults", ())) + 1
    tb_path = f"{led_path}.fault{k}.txt" if led_path else None
'''
A_NOTE_ROW_OLD = '''    ag.led.record(ag.cycle, "SETTLE", "@run", "agent_fault", type=type(e).__name__,
                  message=str(e)[:300], site=site, traceback=tb_path,
                  reads="the agent's own code raised: a defect, recorded and never silent")
    return True
'''
A_NOTE_ROW_NEW = '''    ag.led.record(ag.cycle, "SETTLE", "@run", "agent_fault", type=type(e).__name__,
                  message=str(e)[:300], site=site, traceback=tb_path,
                  **({} if repeat is None else {"repeat": repeat}),
                  reads="the agent's own code raised: a defect, recorded and never silent")
    return True


def end_path(ag: Any, env: Any, game: str, library: str | None, save_only_dir: str | None,
             led_path: str | None, lineage_dir: str | None, fault: bool) -> tuple:
    """play()'s end path: end_run, the library save, the stop-loss and the lineage generation.
    After an agent fault (item 4) each part runs guarded (a failure is a row, never a second
    raise), the ending is agent_fault, and the library is replaced only by a save that loads back.
    (B) runs it on the faulted agent before the fresh one loads what it wrote."""
    part = (lambda f, *a: guarded(ag, f, *a)) if fault else (lambda f, *a: f(*a))
    part(ag.end_run, ledger.AGENT_FAULT if fault else "cap")   # MC2
    saved = None
    if library:
        saved = part(checked_save, ag.gamma, library, env, game) if fault else ag.gamma.save(library)
    saved_only = part(save_only, ag, save_only_dir, game, led_path)
    # (b'-g) the boundary's generation, beside the stop-loss (lineage.py)
    lineage_gen = (part(lineage.write, lineage_dir, ag, game)
                   if lineage._CARRY and lineage_dir else None)
    return saved, saved_only, lineage_gen


def step_or_recover(env: Any, ag: Any, ctx: dict) -> tuple:
    """(B), IN-GAME RECOVERY AFTER AN AGENT FAULT (Isaiah 2026-10-22 12:36-12:37; the design post
    15:13, approved 15:17 with (C3), (C4)). One ag.step(). An Exception from the agent's own code
    (never a BaseException, so a deadline cut is never a fault; never one with a frame inside the
    game's packages, re-raised as before) is recorded (note_fault). Then:
      - the same fault (fault_key) a second time in this game, or TETHER_FAULT_RECOVER off: the
        fault is returned and the game ends into item 4's end path, as without (B);
      - else the faulted agent's end path runs (item 4's checked save), a fresh world is built on
        the SAME wrapper (no RESET: the board as the game holds it) and a fresh agent on the SAME
        ledger loads what was written; only the harness's clock crosses (the cycle after the
        faulted one, the deadline); the faulted agent is dropped.
    ctx: game, cfg, library, lineage_dir, led_path, save_only_dir, palette; "faults" is kept in it.
    Returns (env, ag, acted, fault): fault is None unless the game is to end on it."""
    try:
        return env, ag, ag.step(), None
    except Exception as e:
        if not tether._ERROR_CARRY:
            raise
        seen = ctx.setdefault("faults", [])
        key = fault_key(e)
        repeat = key in seen
        if not note_fault(ag, e, ctx.get("led_path"), k=len(seen) + 1, repeat=repeat):
            raise
        seen.append(key)
        if repeat or not tether._FAULT_RECOVER:
            return env, ag, False, e
    end_path(ag, env, ctx["game"], ctx.get("library"), ctx.get("save_only_dir"),
             ctx.get("led_path"), ctx.get("lineage_dir"), True)
    cycle, deadline, led = ag._fault_cycle + 1, ag.deadline, ag.led
    if ctx.get("keep_faulted") is not None:     # a test's hook: the discard step disabled (r3)
        fresh_env, fresh = env, ctx["keep_faulted"](ag)
        fresh.cycle, fresh.deadline = cycle, deadline
    else:
        fresh_env = world_on(env.w, ctx["game"], ctx["palette"], env.on_frame)
        fresh, _loaded = wire_agent(fresh_env, ctx["game"], ctx.get("cfg"), led,
                                    ctx.get("library"), ctx.get("lineage_dir"),
                                    clock=(cycle, deadline))
    led.record(cycle, "SETTLE", "@run", "fault_recovered", fault=len(seen),
               parent=getattr(fresh, "lineage_parent", None),
               reads="(B): a fresh agent loaded from the checked save goes on in the same game, on "
                     "the board as the game holds it; nothing of the faulted agent's state crossed")
    return fresh_env, fresh, False, None
'''
A_LOOP_OLD = '''    fault = None           # item 4: an agent fault ends the loop into a guarded end path
    for _ in range(cycles):
'''
A_LOOP_NEW = '''    fault = None           # item 4: an agent fault ends the loop into a guarded end path
    ctx = {"game": game, "cfg": cfg, "library": library, "lineage_dir": lineage_dir,
           "led_path": led_path, "save_only_dir": save_only_dir, "palette": palette}
    for _ in range(cycles):
'''
A_STEP_OLD = '''        try:
            acted = ag.step()  # the world notes contact inside `step`, on its own before/after
        except Exception as e:
            if not tether._ERROR_CARRY or not note_fault(ag, e, led_path):
                raise
            fault = e          # item 4: the agent's own code raised; the end path below
            break
'''
A_STEP_NEW = '''        # the world notes contact inside `step`, on its own before/after; (B) recovers a fault
        env, ag, acted, fault = step_or_recover(env, ag, ctx)
        if fault is not None:
            break              # item 4: a repeat (or (B) off): the end path below
'''
A_END_OLD = '''    # item 4: after an agent fault each part of the end path runs guarded (a failure is a row,
    # never a second raise), the game ends as agent_fault, and the library is replaced only by a
    # save that loads back; with no fault every part runs as before
    part = (lambda f, *a: guarded(ag, f, *a)) if fault is not None else (lambda f, *a: f(*a))
    part(ag.end_run, ledger.AGENT_FAULT if fault is not None else "cap")   # MC2
    rows = led.rows()
    g = ag.gamma
    saved = None
    if library:
        saved = part(checked_save, g, library, env, game) if fault is not None else g.save(library)
    saved_only = part(save_only, ag, save_only_dir, game, led_path)
    # (b'-g) the boundary's generation, beside the stop-loss (lineage.py)
    lineage_gen = (part(lineage.write, lineage_dir, ag, game)
                   if lineage._CARRY and lineage_dir else None)
'''
A_END_NEW = '''    saved, saved_only, lineage_gen = end_path(ag, env, game, library, save_only_dir, led_path,
                                              lineage_dir, fault is not None)
    rows = led.rows()
    g = ag.gamma
'''
edit("arc_holdout.py", [(A_WIRE_ENV_OLD, A_WIRE_ENV_NEW), (A_WIRE_TAIL_OLD, A_WIRE_TAIL_NEW),
                        (A_AGENT_OLD, A_AGENT_NEW),
                        (A_NOTE_OLD, A_NOTE_NEW), (A_NOTE_ROW_OLD, A_NOTE_ROW_NEW),
                        (A_LOOP_OLD, A_LOOP_NEW), (A_STEP_OLD, A_STEP_NEW),
                        (A_END_OLD, A_END_NEW)])

# ---------------------------------------------------------------- gate: faults stay visible
edit("gate.py", [
    ("    for fn in (_mode, _steps, _inputs, _routing, _guards, _settlement, _filters, _cuts,\n"
     "               _unreached, _experiment, _refusals, _abandonments, _aliasing, _resolutions):\n",
     "    for fn in (_mode, _steps, _inputs, _routing, _guards, _settlement, _filters, _cuts,\n"
     "               _unreached, _experiment, _refusals, _abandonments, _aliasing, _resolutions,\n"
     "               _faults):\n"),
    ("def _cuts(rows: list[dict]) -> dict | None:\n",
     "def _faults(rows: list[dict]) -> dict | None:\n"
     "    \"\"\"(B). An agent fault is a defect, whatever came after it: a recovered game still FAILS\n"
     "    here, so a fault is never read as a quiet recovery (10-14's R5).\"\"\"\n"
     "    for r in rows:\n"
     "        if r.get(\"event\") == \"agent_fault\":\n"
     "            return _v(\"faults\", AGENT_FAULT, r.get(\"seq\"), str(r.get(\"detail\", {}).get(\"site\")))\n"
     "    return None\n\n\n"
     "def _cuts(rows: list[dict]) -> dict | None:\n"),
    ('RESOLVED_TWICE = "resolved-twice"\n',
     'RESOLVED_TWICE = "resolved-twice"\nAGENT_FAULT = "agent-fault"\n'),
])

# ---------------------------------------------------------------- e4_stream: its call site
edit("harness/mem_store/e4_stream.py", [
    ("env, ag, led, _board, _pal, _loaded = arc_holdout.wire(proxy, \"stream\", led_path=led_path,\n"
     "                                                         lineage_dir=A.lineage)\n",
     "env, ag, led, _board, _pal, _loaded = arc_holdout.wire(proxy, \"stream\", led_path=led_path,\n"
     "                                                         lineage_dir=A.lineage)\n"
     "ctx = {\"game\": \"stream\", \"cfg\": None, \"library\": None, \"lineage_dir\": A.lineage,\n"
     "       \"led_path\": led_path, \"save_only_dir\": None, \"palette\": _pal}   # (B)\n"),
    ("        ag.step()\n        steps += 1\n",
     "        env, ag, _acted, fault = arc_holdout.step_or_recover(env, ag, ctx)   # (B)\n"
     "        if fault is not None:\n"
     "            raise fault\n"
     "        steps += 1\n"),
])

# ---------------------------------------------------------------- test_gate: (f), the rule's defect
edit("tests/test_gate.py", [(
    "def test_unreached_unmeasured():\n",
    "def test_agent_fault():\n"
    "    \"\"\"(B): a fault stays a defect whatever came after it -- a recovered game still refuses.\"\"\"\n"
    "    r = valid()\n"
    "    r += [{\"mode\": \"specified\", \"seq\": 5, \"cycle\": 1, \"step\": \"SETTLE\", \"slot\": \"@run\",\n"
    "           \"event\": \"agent_fault\", \"detail\": {\"type\": \"KeyError\", \"site\": \"tether.py:1\"}},\n"
    "          {\"mode\": \"specified\", \"seq\": 6, \"cycle\": 2, \"step\": \"SETTLE\", \"slot\": \"@run\",\n"
    "           \"event\": \"fault_recovered\", \"detail\": {\"fault\": 1}}]\n"
    "    _refuses(r, gate.AGENT_FAULT)\n"
    "    assert gate.check(r[:5] + r[6:])[\"verdict\"] == gate.PASS   # the recovery row alone passes\n"
    "\n\n"
    "def test_unreached_unmeasured():\n")])

# ---------------------------------------------------------------- conform/arms.py: the row
edit("conform/arms.py", [(
    '    "TETHER_END_RESERVE": "C1 (A)\'s END-PATH RESERVE',
    '    "TETHER_FAULT_RECOVER": "(B), IN-GAME RECOVERY AFTER AN AGENT FAULT (the design post "\n'
    '                            "2026-10-22 15:13; the reviewer 15:17 (C3), (C4)): '
    'arc_holdout.step_or_recover, "\n'
    '                            "at play\'s and e4_stream\'s step: after an agent fault (item 4\'s "\n'
    '                            "row and checked save) a fresh world on the same wrapper (no "\n'
    '                            "RESET) and a fresh agent on the same ledger load the checked "\n'
    '                            "save; only the cycle and the deadline cross; the same fault "\n'
    '                            "again (type + innermost repo frame; a MemoryError by type) ends "\n'
    '                            "the game. OFF: the first fault ends the game, as item 4 alone. "\n'
    '                            "default ON",\n'
    '    "TETHER_END_RESERVE": "C1 (A)\'s END-PATH RESERVE')])
