"""Item 4 in arc_holdout.play: the fault's catch, the guarded end path, the re-raise."""
import sys

sys.dont_write_bytecode = True
p = sys.argv[1] + "/arc_holdout.py"
s = open(p, encoding="utf-8").read()
R = [
    ('''        acted = ag.step()  # the world notes contact inside `step`, on its own before/after
''',
     '''        try:
            acted = ag.step()  # the world notes contact inside `step`, on its own before/after
        except Exception as e:
            if not tether._ERROR_CARRY or not note_fault(ag, e, led_path):
                raise
            fault = e          # item 4: the agent's own code raised; the end path below
            break
'''),
    ('''    if tether._END_RESERVE:
        ag._end_path_t0 = time.perf_counter()    # C1 (A)'s reserve: the end path is timed whole
    ag.end_run("cap")          # MC2: the open level resolves at the game
    rows = led.rows()
    g = ag.gamma
    saved = g.save(library) if library else None
    saved_only = save_only(ag, save_only_dir, game, led_path)
    # (b'-g) the boundary's generation, beside the stop-loss (lineage.py)
    lineage_gen = lineage.write(lineage_dir, ag, game) if lineage._CARRY and lineage_dir else None
''',
     '''    if tether._END_RESERVE:
        ag._end_path_t0 = time.perf_counter()    # C1 (A)'s reserve: the end path is timed whole
    # item 4: after an agent fault each part of the end path runs guarded (a failure is a row,
    # never a second raise), the game ends as agent_fault, and the library is replaced only by a
    # save that loads back; with no fault every part runs as before
    part = (lambda f, *a: guarded(ag, f, *a)) if fault is not None else (lambda f, *a: f(*a))
    part(ag.end_run, ledger.AGENT_FAULT if fault is not None else "cap")   # MC2: resolves at the game
    rows = led.rows()
    g = ag.gamma
    saved = None
    if library:
        saved = part(checked_save, g, library, env, game) if fault is not None else g.save(library)
    saved_only = part(save_only, ag, save_only_dir, game, led_path)
    # (b'-g) the boundary's generation, beside the stop-loss (lineage.py)
    lineage_gen = (part(lineage.write, lineage_dir, ag, game)
                   if lineage._CARRY and lineage_dir else None)
'''),
    ('''    close = getattr(ag.led, "close", None)
    if close is not None:
        close()

    # FILED UNDER WHAT THE AGENT COMPUTED.''',
     '''    close = getattr(ag.led, "close", None)
    if close is not None:
        close()
    if fault is not None:
        raise fault        # item 4: game_one records the error as before, now with the save behind it

    # FILED UNDER WHAT THE AGENT COMPUTED.'''),
    ('''def save_only(ag: Any, out_dir: str | None, game: str, led_path: str | None) -> dict | None:''',
     '''GAME_PACKAGES = ("arc_agi", "arcengine")    # a fault raised inside these is the game's, not ours


def note_fault(ag: Any, e: BaseException, led_path: str | None) -> bool:
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
    if tb_path:
        with open(tb_path, "w", encoding="utf-8", newline="\\n") as fh:
            fh.write("".join(traceback.format_exception(e)))
    ag._faults = [*getattr(ag, "_faults", ()), (type(e).__name__, site)]
    ag._fault_cycle, ag._fault_text = ag.cycle, f"{type(e).__name__}: {e}"
    ag.led.record(ag.cycle, "SETTLE", "@run", "agent_fault", type=type(e).__name__,
                  message=str(e)[:300], site=site, traceback=tb_path,
                  reads="the agent's own code raised: a defect, recorded and never silent")
    return True


def guarded(ag: Any, fn, *a):
    """Item 4: one part of a fault's end path; a failure is recorded and nothing more is written."""
    try:
        return fn(*a)
    except Exception as e:
        ag.led.record(ag.cycle, "SETTLE", "@run", "carry_refused",
                      part=getattr(fn, "__name__", str(fn)), why=f"{type(e).__name__}: {e}"[:300],
                      reads="item 4: this part of the end path failed after an agent fault; "
                            "nothing was written for it")
        return None


def checked_save(g: Any, library: str, env: Any, game: str) -> Any:
    """Item 4: the library saved to a temporary file and loaded back into a fresh Gamma before it
    replaces the library; a save that does not load back leaves the previous one in place."""
    tmp = library + ".tmp"
    out = g.save(tmp)
    gamma.Gamma(env.atoms(), game=game).load(tmp, hold_unbound=lineage._CARRY)
    os.replace(tmp, library)
    return out


def save_only(ag: Any, out_dir: str | None, game: str, led_path: str | None) -> dict | None:'''),
]
for a, b in R:
    assert s.count(a) == 1, a[:70]
    s = s.replace(a, b)
with open(p, "w", encoding="utf-8", newline="\n") as fh:
    fh.write(s)
print("ok")
