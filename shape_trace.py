"""Item 21, THE INSTRUMENT (the reviewer 2026-11-05 r1234): per board, the shape the agent held, its
residual's trend, and when it switched -- read from one run's ledger, one game per ledger, never
pooled across games (Fig 1 :22). It reads the record-only fields TETHER_SHAPE_TRACE writes (family,
board, trend) and the rows beside them (family_demoted, goal_unbundled); it changes no contact
(Fig 11) and never invents a hold the ledger does not name.

    python shape_trace.py runs/<run>.jsonl
"""
from __future__ import annotations

import json
import sys

sys.dont_write_bytecode = True


def _trend(t: dict) -> str:
    return "; ".join(f"{sl} {v['first']}->{v['last']} fell={v['fell']} n={v['n']}"
                     for sl, v in sorted((t or {}).items()))


def trace(rows: list) -> list[str]:
    """The per-board lines, or ["no shape trace"] where the ledger carries no traced hold."""
    picks = [r for r in rows if r.get("event") == "goal_hypotheses"
             and r["detail"].get("pick") and "board" in r["detail"]]
    if not picks:
        return ["no shape trace"]
    holds: dict = {}            # board -> [hold]
    open_: dict = {}            # board -> the hold not yet ended
    board_at = []               # (cycle, board): which board a side row falls on
    for r in sorted((r for r in rows if r.get("event") in (
            "goal_hypotheses", "goal_hypothesis_end", "family_demoted", "goal_unbundled",
            "proposal_gated")),
            key=lambda r: r.get("cycle", 0)):
        d, cy = r["detail"], r.get("cycle", 0)
        if r["event"] == "goal_hypotheses" and d.get("pick") and "board" in d:
            h = {"held": cy, "text": d["pick"], "family": d.get("family"),
                 "under": (d.get("desc") or {}).get("holding"), "side": [],
                 "families": d.get("families")}
            holds.setdefault(d["board"], []).append(h)
            open_[d["board"]] = h
            board_at.append((cy, d["board"]))
        elif r["event"] == "goal_hypothesis_end" and "board" in d:
            h = open_.pop(d["board"], None)
            if h is not None and h["text"] == d.get("text"):
                h.update(ended=cy, why=d.get("why"), by=d.get("by"), trend=d.get("trend"))
        elif r["event"] in ("family_demoted", "goal_unbundled", "proposal_gated") and board_at:
            b = ([d["board"]] if r["event"] == "proposal_gated" and d.get("board") in holds
                 else [bd for c, bd in board_at if c <= cy])
            hs = holds.get(b[-1], []) if b else []
            if hs:
                hs[-1]["side"].append((f"c{cy} {r['event']}", {k: v for k, v in d.items()
                                                    if k not in ("text", "reads")}))
    out = []
    for b in sorted(holds, key=lambda x: (x is None, x)):
        out.append(f"board {b}: {len(holds[b])} hold(s)")
        for i, h in enumerate(holds[b]):
            span = f"c{h['held']}-c{h['ended']}" if "ended" in h else f"c{h['held']}-(held)"
            out.append(f"  {span} {h['text']!r} family={h['family']} under={h['under']}"
                       + (f" ended {h['why']}/{h['by']}" if "ended" in h else ""))
            if h.get("families"):
                out.append("    open by family " + "; ".join(
                    f"{f} {e['n']} cheapest {e['cheapest']!r} @{e['bits']}"
                    for f, e in sorted(h["families"].items())))
            if h.get("trend"):
                out.append(f"    trend {_trend(h['trend'])}")
            for ev, d in h["side"]:
                out.append(f"    {ev} {d}")
            if i + 1 < len(holds[b]) and "ended" in h:
                nxt = holds[b][i + 1]
                out.append(f"    switch +{nxt['held'] - h['ended']} cycles -> {nxt['text']!r} "
                           f"({nxt['family']})")
    return out


def main(path: str) -> None:
    with open(path, encoding="utf-8") as f:
        rows = [json.loads(line) for line in f if line.strip()]
    print("\n".join(trace(rows)))


if __name__ == "__main__":
    main(sys.argv[1])
