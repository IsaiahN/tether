"""The agent's primary stream, verbatim, per cycle -- for reading against a board by hand.

    .venv/Scripts/python.exe transcript.py ka59 24 C:/Users/Admin/Desktop/transcripts

**THE TOOL IS VERSIONED AND THE TRANSCRIPTS ARE NOT**, the same split as the figures pipeline:
they are large, they grow with depth, they are regenerable from any run, and committing them
would store something derivable and churn the diff on every read.

**IT RECONSTRUCTS NOTHING.** `play()` builds a `Ledger` with no path, so the stream is never
written to disk and no parameter exposes one -- so this captures the LEDGER OBJECT and calls its
own `rows()`, which is the serialiser the gate reads. Every field, in the order the build emitted
it. That is `I2`'s rule at the one site it matters most: **wrap the call the build makes; never
rebuild its inputs.** A prose rendering would be a reconstruction with better grammar, and it
would hide exactly the class of error this exists to catch.

**NOTHING IS CURATED.** No filtering to interesting cycles, no summarising runs of similar ones,
no annotation, no type translation, no rounding, no reordering, no collapsing repeats, no dropping
fields that look uninformative. **A cycle where the agent pressed and learned nothing is printed
as the cycle where the agent pressed and learned nothing.** Empty cycles are printed as empty,
because a silent cycle is a cycle nobody can check.

**NOTHING SEAT-SIDE.** The ledger holds what the AGENT emitted. `levels_completed`, the scorecard,
ground truth and harness state are the seat's and none of them is here.

**NOTHING ADDED.** If a value is not emitted today it does not appear here, and **that absence is
a finding to report rather than a gap to patch** -- an emitter written to fill it would be this
tool inventing the evidence it exists to show.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.dont_write_bytecode = True


def _capture(game: str, cycles: int) -> list[dict]:
    """Run the board and hand back the ledger's OWN rows."""
    import ledger

    seen: list = []
    real_init = ledger.Ledger.__init__

    def init(self, *a, **k):
        real_init(self, *a, **k)
        seen.append(self)

    ledger.Ledger.__init__ = init
    try:
        import arc_holdout
        arc_holdout.play(game, cycles=cycles)
    finally:
        ledger.Ledger.__init__ = real_init
    # the agent's ledger is the one that took rows; a bare one would be a different object
    return max((s.rows() for s in seen), key=len, default=[])


def render(rows: list[dict], game: str, cycles: int) -> str:
    out: list[str] = [
        f"# {game} x {cycles} -- the agent's primary stream, verbatim",
        f"# {len(rows)} rows. Nothing filtered, summarised, rounded, reordered or added.",
        f"# Fields are the ledger's own: {sorted({k for r in rows for k in r})}",
        "",
    ]
    if not rows:
        out.append("(no rows -- the agent emitted nothing)")
        return "\n".join(out)

    lo = min(r["cycle"] for r in rows)
    hi = max(r["cycle"] for r in rows)
    by_cycle: dict[int, list[dict]] = {}
    for r in rows:
        by_cycle.setdefault(r["cycle"], []).append(r)

    for c in range(lo, hi + 1):
        got = by_cycle.get(c, [])
        out.append(f"===== cycle {c} =====  ({len(got)} rows)")
        if not got:
            out.append("  (the agent emitted nothing this cycle)")
            out.append("")
            continue
        for r in got:
            head = (f'  seq={r.get("seq")} step={r.get("step")} '
                    f'slot={r.get("slot")} event={r.get("event")}')
            rest = {k: v for k, v in r.items()
                    if k not in ("seq", "step", "slot", "event", "cycle")}
            out.append(head)
            # sort_keys=False: the emission order is part of what is being shown
            out.append("      " + json.dumps(rest, sort_keys=False, default=str))
        out.append("")
    return "\n".join(out)


if __name__ == "__main__":
    if len(sys.argv) < 4:
        print(__doc__.strip().splitlines()[2].strip())
        raise SystemExit(2)
    g, n, dest = sys.argv[1], int(sys.argv[2]), Path(sys.argv[3])
    dest.mkdir(parents=True, exist_ok=True)
    captured = _capture(g, n)
    path = dest / f"{g}_x{n}.transcript.txt"
    path.write_text(render(captured, g, n), encoding="utf-8")
    print(f"{len(captured)} rows -> {path}")
