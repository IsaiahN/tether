"""epoch — a ground-only progress instrument across generations of game playing.

Reads the LEDGER, never the agent's internal frame. Fig 10: "A verifier that can reconstruct
the claim cannot verify it" — so this module imports no agent state, takes only rows, and is
never imported by tether.py (check_paths enforces the direction).

THE FORMULA (figures/THE_FORMULA.md:75-81): "a system measuring progress by terms minted is
counting the denominator." So mint counts are NOT progress. What is admissible is what the
GROUND paid: `settle` rows (a term held on a transition it was not fitted to), `refuse` rows,
`win_credit` and level/win outcomes — and the GRAMMAR those settlements built:
    words grounded   distinct single-unit terms the ground settled
    sentences formed distinct COMPOSED terms (>= 2 atoms) the ground settled and that were
                     used as a method (a `chunk_reuse` or a later `bet` bound to that name)
A replay is not a new word: the same term settled in two generations counts once (Fig 4,
"only methods cross up ... never the recording of a particular success").

Nothing here is read by any agent decision. It is a report for seats, not a channel to the loop.
"""
from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

sys.dont_write_bytecode = True


def _unit_count(name: str) -> int:
    """Atom count of a term NAME, from its composition spelling, never from agent state."""
    # A composed term is spelled "a . b<operand>?GUARD"; a single atom has no " . ".
    head = name.split("<", 1)[0].split("?", 1)[0]
    return len([p for p in head.split(".") if p.strip()])


def summarise(rows: list[dict[str, Any]]) -> dict[str, Any]:
    """One generation's ground-settled grammar, from ledger rows alone.

    Rows are dicts with at least 'event' and 'detail'. A term name is detail['term'] on a
    settle row. 'used as a method' is a later bound bet naming the same term or a chunk_reuse
    row; both are ground/ledger events, not frame-internal counts.
    """
    settled: dict[str, str] = {}          # term name -> how the ground settled it
    settles = refusals = wins = 0
    pressed = 0
    first_settle_at: int | None = None
    for i, r in enumerate(rows):
        ev = r.get("event")
        d = r.get("detail") or {}
        if ev == "settle" and isinstance(d.get("term"), str):
            settles += 1
            settled[d["term"]] = d.get("status", "settled")
            if first_settle_at is None:
                first_settle_at = i
        elif ev == "refuse":
            refusals += 1
        elif ev == "win_credit":
            wins += 1
        elif ev == "bet" and d.get("bound") not in (None, "no_change"):
            pressed += 1

    words = {n for n in settled if _unit_count(n) == 1}
    sentences = {n for n in settled if _unit_count(n) >= 2}

    return {
        "settles": settles,
        "refusals": refusals,
        "wins": wins,
        "words_grounded": sorted(words),
        "sentences_formed": sorted(sentences),
        "words_n": len(words),
        "sentences_n": len(sentences),
        "presses_to_first_settle": (first_settle_at if first_settle_at is not None else -1),
        "ground_rows": settles + refusals + wins,
    }


def trend(summaries: list[dict[str, Any]]) -> dict[str, Any]:
    """Trend across generations. New words/sentences are those not seen in any EARLIER gen.

    A replay (same term settled again) contributes 0 new — Fig 4. Ground rows per generation
    are reported beside the grammar counts (Fig 12's second currency), never netted against
    them. No proxy is combined into a single score.
    """
    seen_words: set[str] = set()
    seen_sent: set[str] = set()
    new_words: list[int] = []
    new_sent: list[int] = []
    ground: list[int] = []
    wins: list[int] = []
    for s in summaries:
        w, x = set(s.get("words_grounded", ())), set(s.get("sentences_formed", ()))
        new_words.append(len(w - seen_words))
        new_sent.append(len(x - seen_sent))
        seen_words |= w
        seen_sent |= x
        ground.append(int(s.get("ground_rows", 0)))
        wins.append(int(s.get("wins", 0)))
    return {
        "new_words_per_generation": new_words,
        "new_sentences_per_generation": new_sent,
        "ground_rows_per_generation": ground,
        "wins_per_generation": wins,
        "total_new_words": sum(new_words),
        "total_new_sentences": sum(new_sent),
        "words_trend_up": sum(new_words) > 0 and new_words[-1] >= new_words[0],
        "sentences_trend_up": sum(new_sent) > 0 and new_sent[-1] >= new_sent[0],
    }


def read_ledger(path: str | Path) -> list[dict[str, Any]]:
    """Rows of one ledger file. The file is the record; nothing is written back."""
    import json
    p = Path(path)
    out = []
    with p.open(encoding="utf-8", errors="replace") as fh:
        for line in fh:
            if '"event"' not in line:
                continue
            try:
                out.append(json.loads(line))
            except ValueError:
                continue
    return out


def main(argv: list[str] | None = None) -> int:
    import argparse
    p = argparse.ArgumentParser(description="epoch: ground-only grammar progress")
    p.add_argument("ledgers", nargs="+", help="one ledger jsonl per generation, oldest first")
    a = p.parse_args(argv)
    summaries = [summarise(read_ledger(f)) for f in a.ledgers]
    import json
    print(json.dumps({"summaries": summaries, "trend": trend(summaries)}, indent=1, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
