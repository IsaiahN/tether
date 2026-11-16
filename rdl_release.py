"""RDL Piece 2: the release schedule (C4), the release base layer, and codified reach.

Spec: docs/03-DESIGN/RDL_BUILD_SPEC_2026-11-16.md, "Piece 2". Design:
docs/05-RESEARCH/40-WATSON_2026-11-13_RECURSIVE_DIFFUSION_LEARNING.md (C4, "The release base
layer", "One pushback, on the bridle", "Codify reach").

THIS MODULE SETS SEARCH PRIORITY ONLY: NEVER REACH, NEVER STANDING. It answers "where does search
look first". It adds nothing to the library, makes nothing reachable (reach is the agent's closure,
by derivation), and writes no standing (standing is only a term's own record with the board).
Tier, release and the reach policy order a lookup; the ground alone settles.

The figures it implements (quoted from the design's citations):
  Fig 7 :37-39  "Progress per handoff has two factors. Zero either and the chain runs in place:
                the bracket's fidelity across the handoff; the ground's pressure on the room."
                -> C4: tier k is released by what the ground has SETTLED at tier k - 1, not by
                the clock. The bridle is the settled count per tier (primary); age is only a
                tiebreak inside `priority` and is never a release trigger ("A store can grow old
                without being pressed": the design's one pushback, on the bridle).
  Fig 12 :101   "... as the vocabulary of bonds grows, and only then." -> the next tier is
                offered only once the one below it has paid.
  Fig 6 :32     "An instrument is not built from a description. It is improved from a worse
                instrument already returning something." -> the reach policy is READ OFF the
                lineage's own ledger rows, never designed from theory.
  Fig 4 :23     "upward: a method that can be reapplied. Never the recording of a particular
                success." -> what is codified is an ordered cue table (a method), keyed by
                (corpus, tier, cluster), never a pid list replaying what worked once.
  Fig 9 :60     "Use filters for the budget and witnesses for the verdict. Never let a filter
                hand you a verdict." -> release and policy are filters on the search budget;
                the verdict stays with the board.

The release base layer (40, "The release base layer"): for fringe release the inherited priors
count as settled, so tier 1 (built directly on them) is released at once. That is priority, not
standing. `inherited_settled=False` removes the base layer, and then tier 1 waits like any other
tier (the must-fail in tests/test_rdl_release.py shows the base layer is what releases it).

No import of tether and none of rdl_store at module level: every function takes any object with
the attributes pid, tier, stage, source (a dict with "corpus"), attaches (and bonds for the C2
fallback), so Piece 1 and Piece 2 build in parallel.
"""
from __future__ import annotations

from collections.abc import Callable, Iterable

# anchor: the project's MIN_REPEAT (self_family.MIN_REPEAT, "one observation is a coincidence"),
# REUSED rather than a new constant (spec Piece 2): a tier opens once the tier below it has been
# settled by the ground at least twice. If it needs to be 3, that is a finding, not a knob.
MIN_SETTLED = 2

EVENTS = ("rdl_offer", "rdl_settle", "rdl_refuse")
_FIELD = {"rdl_offer": "offered", "rdl_settle": "settled", "rdl_refuse": "refused"}


def _usable_c2(p) -> bool:
    """C2 exactly as the spec defines it (rdl_store.usable): at least one bond AND one attach."""
    return bool(p.bonds) and bool(p.attaches)


def _corpus(p) -> str:
    return str((p.source or {}).get("corpus", ""))


def _settled_at(stats: dict, tier: int) -> int:
    """The settled count at `tier`, summed over sources (corpora)."""
    return sum(int(v.get("settled", 0)) for (_c, t), v in stats.items() if int(t) == tier)


def released(preloads: Iterable, stats: dict | None, inherited_settled: bool = True,
             usable: Callable | None = None) -> set[str]:
    """C4: the pids released to search priority.

    Tier 1 is released at once when `inherited_settled` (the base layer: the inherited priors,
    tier 0, count as settled for the fringe -- priority, not standing). Tier k > 1 (and tier 1
    without the base layer) is released when the settled count at tier k - 1, summed over
    sources, is at least MIN_SETTLED. Only usable preloads are released (`usable(p)`, else the
    C2 fallback `bool(p.bonds) and bool(p.attaches)`). Age is never a release trigger."""
    stats = stats or {}
    ok = usable if usable is not None else _usable_c2
    open_tier: dict[int, bool] = {}
    out = set()
    for p in preloads:
        k = int(p.tier)
        if k not in open_tier:
            if k == 1 and inherited_settled:
                open_tier[k] = True
            else:
                open_tier[k] = _settled_at(stats, k - 1) >= MIN_SETTLED
        if open_tier[k] and ok(p):
            out.add(p.pid)
    return out


def stats_from_rows(rows: Iterable[dict]) -> dict:
    """`{(corpus, tier): {"offered": n, "settled": n, "refused": n}}` from ledger rows
    (`{"event", "detail": {pid, tier, corpus, cluster}, "cycle", "slot"}`); other events are
    ignored."""
    out: dict = {}
    for r in rows:
        ev = r.get("event")
        if ev not in _FIELD:
            continue
        d = r.get("detail") or {}
        key = (str(d.get("corpus", "")), int(d.get("tier", 0)))
        rec = out.setdefault(key, {"offered": 0, "settled": 0, "refused": 0})
        rec[_FIELD[ev]] += 1
    return out


def cue_text(cue: tuple) -> str:
    """A cue's text, the last tiebreak of the policy: corpus|tier|cluster."""
    return "|".join(str(x) for x in cue)


def reach_policy(rows: Iterable[dict]) -> list[tuple]:
    """Codified reach (40 "Codify reach"; Take The Best): an ordered symbolic table read off the
    lineage's own rows, never weights. Each entry is `(cue, tried, paid, validity)` with cue
    `(corpus, tier, cluster)`. paid = rdl_settle rows; tried = ended trials, rdl_settle +
    rdl_refuse rows (an rdl_offer with no outcome yet is a cue seen, not a trial -- the same
    "ended holds" the agent's _b2_cues counts). validity = (paid + 1) / (tried + 2), the form of
    _b2_cues. Order: validity descending, then tried descending, then the cue's text."""
    tally: dict[tuple, list[int]] = {}
    for r in rows:
        ev = r.get("event")
        if ev not in _FIELD:
            continue
        d = r.get("detail") or {}
        cue = (str(d.get("corpus", "")), int(d.get("tier", 0)), str(d.get("cluster", "")))
        tp = tally.setdefault(cue, [0, 0])
        if ev == "rdl_settle":
            tp[0] += 1
            tp[1] += 1
        elif ev == "rdl_refuse":
            tp[0] += 1
    table = [(cue, t, p, (p + 1) / (t + 2)) for cue, (t, p) in tally.items()]
    table.sort(key=lambda e: (-e[3], -e[1], cue_text(e[0])))
    return table


def _clusters(p) -> tuple:
    """The clusters a preload is cued by, if it names them (`cluster` / `clusters` attribute or
    source["cluster"]); empty means "any cluster of its (corpus, tier)"."""
    c = getattr(p, "clusters", None) or getattr(p, "cluster", None) \
        or (p.source or {}).get("cluster")
    if not c:
        return ()
    return (str(c),) if isinstance(c, str) else tuple(str(x) for x in c)


def priority(preload, policy: list[tuple], age) -> tuple:
    """The search-priority sort key, lower first: (policy rank of its cue, tier, -age, pid).
    The rank is the first policy entry whose cue matches the preload's (corpus, tier, cluster);
    a preload naming no cluster matches any cluster of its (corpus, tier); no match ranks after
    every entry (len(policy)). Age only breaks ties (older first), never releases."""
    corpus, tier, cl = _corpus(preload), int(preload.tier), _clusters(preload)
    rank = len(policy)
    for i, e in enumerate(policy):
        c, t, k = e[0]
        if c == corpus and int(t) == tier and (not cl or k in cl):
            rank = i
            break
    return (rank, tier, -(age or 0), preload.pid)


def merge_stats(a: dict | None, b: dict | None) -> dict:
    """Summed increments (the lineage carry adds a generation's increments to its ancestors').
    Neither input is mutated."""
    out: dict = {}
    for src in (a or {}, b or {}):
        for key, rec in src.items():
            dst = out.setdefault(key, {})
            for f, n in rec.items():
                dst[f] = dst.get(f, 0) + int(n)
    return out
