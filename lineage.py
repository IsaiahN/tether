"""(b'-g) THE LINEAGE CARRY (Fig 12, Fig 10, Fig 4, Fig 6; the reviewer 2026-10-14 20:18, 20:22;
Isaiah 2026-10-14 11:05 "whats in the library STAYS in the library", 19:05).

At every game and run boundary the lineage writes a GENERATION, and the next instance loads the
chain. ONE PATH: an in-process game is a boundary like any other, so nothing is handed on in memory.

A generation holds only what CHANGED since its parent: new term rows, status changes, new settle/
refute evidence, the vindication tail, changed book keys, new inventions, and the instance's dormant
record. The library at load is the chain FOLDED, root to tip.

THE FORMAT HAS NO DELETION (Isaiah 11:05). No row type removes a key: a later status row for a key
supersedes an earlier one in the folded view, and the earlier one stays in its file.

A generation is named by the hash of its own bytes and names its parent's. It is never overwritten.
More than one tip, or a link that does not verify, RAISES with the tips or the bad link named: never
a silent pick of a tip, never a silent cold start. An empty or absent folder is the root, said so.

The evidence and the dormant record are the RECORD: written and folded, never read back into
standing or into a live store (standing is 7i's; the kind forms are (b'-l) phase 2's).
ANNOTATED 2026-10-15 (7i, the reviewer 19:04, 19:36): under TETHER_SETTLED_CORE the folded
evidence IS read back into standing at load (Gamma.replay), globally, never per slot; the
record itself is unchanged. The dormant record is still not read back."""
from __future__ import annotations

import dataclasses
import hashlib
import heapq
import json
import os
import time
from collections import Counter
from pathlib import Path
from typing import Any

import armflag
import gamma
import sensors

# default ON (Isaiah 2026-10-15 07:53); the switch is kept for the checklist's culprit isolation.
_CARRY = armflag.arm("TETHER_LINEAGE_CARRY", default=True)   # _UPPER, so the @run header records it
# THE BOUNDARY WRITE (the reviewer 2026-10-15 06:46, 07:23, 07:32; Isaiah 06:20): under the carry,
# a generation at every level clear and death too, so a stop loses at most the current level.
# default ON (Isaiah 2026-10-15 07:53); the switch is kept for the checklist's culprit isolation.
_BOUNDARY = armflag.arm("TETHER_LINEAGE_BOUNDARY", default=True)
# S1g, THE ASKED RECORD (Isaiah 2026-10-15 13:26, option B; the reviewer 13:27, 13:28): under the
# slot filter a generation carries WHICH QUESTIONS WERE ASKED, never the bound answers; the next
# process rebuilds each answer from the carried index by the existing binds. A5: an animal keeps
# the map and the memory of where it has been, and walks the path again when it needs it.
# default ON (Isaiah 2026-10-15 07:53); the switch is kept for the checklist's culprit isolation.
_RECORD = armflag.arm("TETHER_CARRY_RECORD", default=True)
# ONE PASS (the reviewer 2026-10-19 06:09 d, 06:13): load reads and folds the memory saves once;
# head()'s pass is the same chain and the same fold, read twice. Default ON (the reviewer 06:35: its
# compare passed, a byte-identical save); the switch is kept as a stop-gap until the store loads.
_ONE_PASS = armflag.arm("TETHER_ONE_PASS", default=True)
# THE CONSOLIDATED MEMORY (the reviewer 2026-10-19 06:13-07:35; Isaiah 06:12): load reads the
# memory folder's store (lineage_store.py) instead of re-reading every save; a folder the store
# cannot answer exactly loads from the archive as before. Default ON (Isaiah 2026-10-19 17:03 "turn
# it on"): OFF, every load is the saves' fold (14.35 GiB on the E4 life, over B); ON, that fold is
# reached only on a refusal. TETHER_MEMORY_STORE=0 is the old path.
_MEMORY_STORE = armflag.arm("TETHER_MEMORY_STORE", default=True)
# COMPRESSION L1 + L6a + L2 (the reviewer 2026-10-20 11:06, 11:13; Isaiah 05:02 "compression is
# required on all levels when passing"): every save file written zlib-6 under the hash of its
# UNCOMPRESSED bytes; the asked record written in its readers' own form (form 3: a tally per
# (key, role, slot class) + the whole pairs); the in-game counter folded at ask. OFF: raw form 2.
_COMPRESS = armflag.arm("TETHER_COMPRESS", default=True)
# S6 H, THE STORE HEALS AT OPEN (the reviewer 2026-10-19; the K crash runs): (1) a store failing
# its cheap check WITH a WAL is checkpointed (TRUNCATE) and checked again, size and quick_check --
# committed pages still in the WAL make page_count exceed the file, so a correct store read as
# short and the load fell back to the saves' fold; (2) a store still failing is SET ASIDE (renamed
# .dead-<UTC>, never deleted) and rebuilt from the saves by catch_up, as a folder with no store
# already is. The load report carries what was done. OFF: as 753339c
_STORE_HEAL = armflag.arm("TETHER_STORE_HEAL", default=True)
PREFIX = "gen_"


def _key(row: dict) -> str:
    """A term row's composition (atom chain, guard, operand tree): what load dedups on. Never a
    row's identity in the record, which is (born, handle) below."""
    return json.dumps([row["atoms"], row.get("guard"), row.get("operand_term")])


def _rid(row: dict) -> tuple:
    """A row's identity in the lineage: its birth handle, qualified by the generation it was
    first written in, so two games' same-text handles never fold together (the reviewer 20:45)."""
    return (row["born"], row.get("handle"))


def enc(x: Any) -> Any:
    """Tagged JSON for the dormant record, so it reads back equal: tuples, sets, non-str dict keys,
    NOT_RESOLVED and gamma.Standing keep their types. Anything else unknown raises."""
    if x is sensors.NOT_RESOLVED:
        return {"__nr__": 1}
    if isinstance(x, dict):
        return {"__d__": [[enc(k), enc(v)] for k, v in x.items()]}
    if isinstance(x, tuple):
        return {"__t__": [enc(v) for v in x]}
    if isinstance(x, (set, frozenset)):
        tag = "__fs__" if isinstance(x, frozenset) else "__s__"
        return {tag: sorted((enc(v) for v in x), key=lambda v: json.dumps(v, sort_keys=True))}
    if isinstance(x, list):
        return [enc(v) for v in x]
    if isinstance(x, gamma.Standing):
        return {"__standing__": {f.name: enc(getattr(x, f.name)) for f in dataclasses.fields(x)}}
    if x is None or isinstance(x, (bool, int, float, str)):
        return x
    raise Unencodable(type(x).__name__)


class Unencodable(TypeError):
    """enc met a type it has no form for; `.type` names it (write records it, item by item)."""

    def __init__(self, tname: str) -> None:
        super().__init__(f"lineage.enc: no form for {tname}")
        self.type = tname


def dec(x: Any) -> Any:
    if isinstance(x, list):
        return [dec(v) for v in x]
    if not isinstance(x, dict):
        return x
    if "__nr__" in x:
        return sensors.NOT_RESOLVED
    if "__d__" in x:
        return {dec(k): dec(v) for k, v in x["__d__"]}
    if "__t__" in x:
        return tuple(dec(v) for v in x["__t__"])
    if "__s__" in x:
        return {dec(v) for v in x["__s__"]}
    if "__fs__" in x:
        return frozenset(dec(v) for v in x["__fs__"])
    if "__standing__" in x:
        return gamma.Standing(**{k: dec(v) for k, v in x["__standing__"].items()})
    raise TypeError(f"lineage.dec: an untagged object {sorted(x)[:4]}")


def _parents(g: dict) -> list[str]:
    """A generation's parents: a MERGE generation names several ("parents"); every other names
    one ("parent", unchanged since (b'-g), so its bytes and hash are what they were) or none."""
    if "parents" in g:
        return list(g["parents"])
    return [g["parent"]] if g.get("parent") else []


def _hazard_families(hz: Any) -> dict:
    """E2: the parts of 3a's hazard that are TEMPLATES and so may cross a boundary -- the world
    counts by kind and by actor, the own counts by kind, and the actor trust -- each the live
    Counter, never a copy. Spots are one board's and stay in the game."""
    return {"world_kind": hz.world["kind"], "world_actor": hz.world["actor"],
            "own_kind": hz.own["kind"], "near": hz.near, "away": hz.away}


def _dumps(x: Any) -> bytes:
    """The one form every lineage file is written in (S1f, the reviewer 2026-10-15 13:01): sorted
    keys and compact separators (indent=1 was 42% of the bytes, the 12:59 read). Every file is
    checked against the hash of its own bytes, so a file written indented still loads and
    verifies; a new file's name differs because its bytes do, its content is the same."""
    return json.dumps(x, sort_keys=True, separators=(",", ":")).encode("utf-8")


def _store_bytes(raw: bytes) -> bytes:
    """L2: what a save file holds on disk -- zlib-6 of its bytes under TETHER_COMPRESS. The name
    and every hash stay those of the uncompressed bytes (lineage_store.file_bytes reads both)."""
    import zlib
    return zlib.compress(raw, 6) if _COMPRESS else raw


def _read(d: Path) -> dict[str, dict]:
    """Every generation in `d`, each verified against its own name; raises on a bad hash or a
    parent that is not in the folder."""
    import lineage_store as ls
    gens: dict[str, dict] = {}
    for f in sorted(d.glob(f"{PREFIX}*.json")):
        raw = ls.file_bytes(f)
        h = hashlib.sha256(raw).hexdigest()[:16]
        if f.stem != PREFIX + h:
            raise ValueError(f"lineage: {f.name} does not hash to its name ({h})")
        gens[h] = json.loads(raw)
    bad = {h: p for h, g in gens.items() for p in _parents(g) if p not in gens}
    if bad:
        raise ValueError(f"lineage: a parent that is not in the chain: {bad}")
    return gens


def _tips(gens: dict[str, dict]) -> list[str]:
    named = {p for g in gens.values() for p in _parents(g)}
    return sorted(set(gens) - named)


def _topo(gens: dict[str, dict]) -> list[str]:
    """Parents before children, ties broken by hash: one fixed order for a DAG, and for a linear
    chain the root-to-tip order (b'-g) read."""
    kids: dict[str, list[str]] = {h: [] for h in gens}
    need = {h: len(_parents(g)) for h, g in gens.items()}
    for h, g in gens.items():
        for q in _parents(g):
            kids[q].append(h)
    ready = [h for h, n in need.items() if n == 0]
    heapq.heapify(ready)
    out = []
    while ready:
        h = heapq.heappop(ready)
        out.append(h)
        for k in kids[h]:
            need[k] -= 1
            if not need[k]:
                heapq.heappush(ready, k)
    return out


def _ancestors(gens: dict[str, dict], h: str) -> set[str]:
    """`h` and every generation it descends from."""
    seen, todo = set(), [h]
    while todo:
        x = todo.pop()
        if x not in seen:
            seen.add(x)
            todo.extend(_parents(gens[x]))
    return seen


def _chain(d: Path) -> list[tuple[str, dict]]:
    """Every generation in `d`, parents before children, each verified against its own name.
    Raises on a bad hash, a missing parent, more than one tip (N3), or a generation the tip does
    not descend from. Branches join only through a MERGE generation (merge), never by a pick."""
    gens = _read(d)
    if not gens:
        return []
    tips = _tips(gens)
    if len(tips) != 1:
        roots = sorted(h for h, g in gens.items() if not _parents(g))
        raise ValueError(f"lineage: not one chain (roots {roots}, tips {tips}); branches join "
                         "only through a merge generation (lineage.merge)")
    held = _ancestors(gens, tips[0])
    if len(held) != len(gens):
        raise ValueError(f"lineage: {len(gens) - len(held)} generation(s) off the chain")
    return [(h, gens[h]) for h in _topo(gens)]


def _keyed(out: dict, field: str, g: dict, h: str, anc: dict, hist: dict, heads: dict) -> None:
    """A keyed field of the fold (book, invented) under the status rule: a value supersedes only
    one its generation descends from. Branches that disagree keep the value from before the
    split (absent if there was none) and record both under "contested_<field>"."""
    for key, v in g[field].items():
        k = (field, key)
        hist.setdefault(k, []).append((h, v))
        heads[k] = {q for q in heads.get(k, set()) if q not in anc[h]} | {h}
        if len(heads[k]) == 1:
            out[field][key] = v
            continue
        common = set.intersection(*(anc[q] for q in heads[k]))
        pre = [x for q, x in hist[k] if q in common]
        if pre:
            out[field][key] = pre[-1]
        else:
            out[field].pop(key, None)
        seen = out.setdefault(f"contested_{field}", {}).setdefault(key, [])
        for q, x in hist[k]:
            if q in heads[k] and {"gen": q, "value": x} not in seen:
                seen.append({"gen": q, "value": x})


def fold(chain: list[tuple[str, dict]]) -> dict:
    """The chain read as one library, root to tip. Every row is kept, each stamped with the
    generation it was first written in ("born"); nothing is removed (N2)."""
    rows: dict[tuple, dict] = {}
    out = {"terms": [], "invented": {}, "vindication": [], "book": {}, "evidence": [],
           "dormant": []}
    anc: dict[str, set] = {}
    # per row: every (generation, admitted) set on it, in fold order, and the setters no later
    # status descends from. One head is the linear case; two or more are branches that disagree
    hist: dict[tuple, list] = {}
    heads: dict[tuple, set] = {}
    khist: dict[tuple, list] = {}     # the same, for book keys and invented names
    kheads: dict[tuple, set] = {}
    for h, g in chain:
        anc[h] = {h}.union(*(anc[q] for q in _parents(g)))
        for r in g["terms"]:
            row = {**r, "born": h}
            rows[_rid(row)] = row
            hist[_rid(row)], heads[_rid(row)] = [(h, row.get("admitted"))], {h}
        for s in g["status"]:
            k = (s["born"], s["handle"])
            row = rows[k]
            hist[k].append((h, s["admitted"]))
            heads[k] = {q for q in heads[k] if q not in anc[h]} | {h}
            if len(heads[k]) == 1:
                row["admitted"] = s["admitted"]
                continue
            # CONTESTED (Fig 6, Open): branches set this row differently and neither descends from
            # the other. Both are kept; the row reads its value from before the split, never the
            # one fold order happened to put last. A later descendant of both supersedes as usual.
            common = set.intersection(*(anc[q] for q in heads[k]))
            row["admitted"] = next(a for q, a in reversed(hist[k]) if q in common)
            seen = row.setdefault("contested", [])
            for q, a in hist[k]:
                if q in heads[k] and {"gen": q, "admitted": a} not in seen:
                    seen.append({"gen": q, "admitted": a})
        _keyed(out, "invented", g, h, anc, khist, kheads)
        out["vindication"].extend(g["vindication_tail"])
        _keyed(out, "book", g, h, anc, khist, kheads)
        out["evidence"].extend(g["evidence"])
        out["dormant"].extend(dec(g["dormant"]))
    out["terms"] = list(rows.values())
    return out


def head(d: str | Path) -> tuple[str | None, dict]:
    """The tip's hash and the fold. An absent or empty folder is the ROOT: (None, an empty fold)."""
    p = Path(d)
    chain = _chain(p) if p.is_dir() else []
    return (chain[-1][0] if chain else None), fold(chain)


def _ksorted(rows) -> list:
    """The kind lists sorted by a TOTAL order: a delta kind's third element is an int on some
    keys and a str on others (ar25, E4a 2026-10-18); plain sorting compares element by element."""
    return sorted(rows, key=lambda x: json.dumps(x, sort_keys=True, default=str))


def _store_base(p: Path, parent: str | None) -> tuple[Any, dict] | str:
    """Under TETHER_MEMORY_STORE: the parent's fold read from the store (a lookup), when the store's
    tip IS the parent; otherwise the reason the archive's O(life) re-fold is used instead."""
    import lineage_store as ls
    try:
        con = ls.open_store(p)
    except ls.Refused as e:
        return f"open refused: {e}"[:300]
    try:
        ls.catch_up(con, p)
        tip = con.execute("SELECT v FROM meta WHERE k='last_merged'").fetchone()
        if (tip[0] if tip else None) != parent:
            con.close()
            return f"the store's tip {tip[0] if tip else None} is not the parent {parent}"
        f = json.loads((con.execute("SELECT v FROM blob WHERE k='fold'").fetchone() or ["{}"])[0])
        nv = con.execute("SELECT v FROM meta WHERE k='n_vindication'").fetchone()
    except ls.Refused as e:
        con.close()
        return f"catch_up refused: {e}"[:300]
    except BaseException:
        con.close()
        raise
    # write() reads only the LENGTH of the stored vindication (schema 4; the reviewer 11:27)
    return con, {"terms": list(f.get("rows", {}).values()),
                 "n_vindication": int(nv[0] if nv else 0),
                 "book": f.get("book", {}), "invented": f.get("invented", {})}


def _fsync(f: Path) -> None:
    with open(f, "r+b") as fh:
        os.fsync(fh.fileno())


def write(d: str | Path, ag: Any, game: str, sleep: bool = True) -> dict:
    """The boundary's generation: only what changed since the parent the instance LOADED
    (ag.lineage_parent), against that parent's fold. Named by its own hash; never overwritten.
    Under TETHER_MEMORY_STORE the parent's fold is a store lookup, and the save is merged into the
    store after its archive files are written and synced; `sleep` (a game's end, never a boundary
    inside a game) also runs the store's checkpoint."""
    held: list = []
    try:
        return _write(d, ag, game, sleep, held)
    finally:    # the store's connection is closed on every path, an error's included
        for con in held:
            con.close()


def _write(d: str | Path, ag: Any, game: str, sleep: bool, held: list) -> dict:
    p = Path(d)
    p.mkdir(parents=True, exist_ok=True)
    parent = getattr(ag, "lineage_parent", None)
    sb = _store_base(p, parent) if _MEMORY_STORE else None
    if isinstance(sb, tuple):
        store_con, base = sb
        held.append(store_con)
    else:
        store_con = None
        if sb is not None:
            # S5 (the reviewer 08:03 3a): the arm fell back to the O(life) re-fold; never silent
            _c, _s, _lv = ag._boundary_key("@lineage")
            ag.led.record(_c, "SETTLE", _s, "store_refold", **_lv, reason=sb,
                          reads="the save's base re-folded from the archive, O(life)")
        chain = _chain(p)
        # the parent and what it descends from, in fold order (a DAG has no prefix to slice)
        keep = _ancestors(dict(chain), parent) if parent else set()
        upto = [(h, g) for h, g in chain if h in keep]
        base = fold(upto)
        base["n_vindication"] = len(base["vindication"])
    prev = {_rid(r): r for r in base["terms"]}
    blob = ag.gamma.blob(with_names=True)
    terms, status = [], []
    # under the boundary arm: what THIS instance already wrote, so a later write in the same game
    # carries only what is new (F3); OFF, both are empty and the write is as before
    written = getattr(ag, "_lineage_written", {}) if _BOUNDARY else {}
    marks = getattr(ag, "_lineage_marks", {}) if _BOUNDARY else {}
    new_names = []
    for r in blob["terms"]:
        # NEW = minted by this instance; a term it LOADED from the lineage carries its identity
        # in carried (born, handle), and only a non-marker change of its status is written (N1).
        name = r.pop("name")
        if gamma._REPLAY_UNIT:
            r["was"] = name     # R7i: the replay finds the term load installs from this row
        c = ag.gamma.carried.get(name) or written.get(name) or {}
        rid = (c.get("born"), c.get("handle"))
        if rid not in prev:
            terms.append(r)
            new_names.append((name, r.get("handle")))
        elif r.get("admitted") not in (None, gamma.IMPORTED, prev[rid].get("admitted")):
            status.append({"born": rid[0], "handle": rid[1], "admitted": r["admitted"]})
    # THE DORMANT RECORD ITEM BY ITEM (the reviewer 21:14, I3): an item enc has no form for is
    # not written, and is named; it never costs the generation its terms, status or evidence.
    dormant, refused = [], []
    d0, e0 = marks.get("dormant", 0), marks.get("evidence", 0)
    dormant_all = getattr(ag, "_dormant", [])
    for i, item in enumerate(dormant_all[d0:], d0):
        try:
            dormant.append(enc(item))
        except Unencodable as e:
            refused.append({"i": i, "type": e.type})
    gen = {"lineage": 1, "parent": parent, "game": game, "terms": terms, "status": status,
           "evidence": list(ag.gamma.evidence)[e0:],
           "vindication_tail": list(blob["vindication"])[base["n_vindication"]:],
           "book": {k: v for k, v in blob["book"].items() if base["book"].get(k) != v},
           "invented": {n: r for n, r in blob["invented"].items() if n not in base["invented"]},
           "dormant": dormant, "dormant_refused": refused}
    # the being's seed and the generation it lived (HOLD_SEED, the reviewer 15:04), so the next
    # process continues it and a replay can read it; OFF writes neither, as before
    if getattr(ag, "seed_source", "constant") != "constant":
        gen["seed"], gen["generation"] = ag.seed, ag.generation
    import tether
    if tether._7L_KIND:
        # 7l: the kinds asked since the last write, and the episodes since it (written through)
        new_kinds = getattr(ag, "_kind_landed", set()) - getattr(ag, "_kinds_carried", set())
        gen["kinds_landed"] = sorted([k, r, list(ko), list(kx)] for k, r, ko, kx in new_kinds)
        gen["episodes"] = list(getattr(ag, "_kind_episodes", [])
                               [getattr(ag, "_kind_episode_mark", 0):])
        if tether._CONSOLIDATE:
            # CONSOLIDATION (the reviewer 04:43 2a-2b): each key's landings since the last write,
            # and the latest landing of each key landed since it (7l and K1); summed / latest at
            # load
            was_n = getattr(ag, "_kn_written", {})
            gen["kinds_landed_n"] = sorted(
                [k, r, list(ko), list(kx), n - was_n.get((k, r, ko, kx), 0)]
                for (k, r, ko, kx), n in ag._kind_landed_n.items()
                if n > was_n.get((k, r, ko, kx), 0))
            gen["kinds_last"] = sorted([k, r, list(ko), list(kx), *v]
                                       for (k, r, ko, kx), v in ag._kind_last.items()
                                       if ag._kind_landed_n[(k, r, ko, kx)] >
                                       was_n.get((k, r, ko, kx), 0))
            was_dk2 = getattr(ag, "_kdk_written", {})
            gen["kinds_dk_last"] = _ksorted([list(d_), k, list(t_), *v]
                                          for (d_, k, t_), v in ag._kdk_last.items()
                                          if ag._kind_landed_dk[(d_, k, t_)] >
                                          was_dk2.get((d_, k, t_), 0))
            gen["kinds_by_class"] = {**dict(ag._kind_cls),
                                     **{f"{c}_keys": len(v) for c, v in ag._kind_cls_keys.items()}}
    if tether._DELTA_KIND and hasattr(ag, "_kind_landed_dk"):
        # K1: the landings with their delta kind since the last write; the load sums the chain
        was_dk = getattr(ag, "_kdk_written", {})
        gen["kinds_landed_dk"] = _ksorted(
            [list(dk_), k, list(tg), n - was_dk.get((dk_, k, tg), 0)]
            for (dk_, k, tg), n in ag._kind_landed_dk.items()
            if n > was_dk.get((dk_, k, tg), 0))
        was_off = getattr(ag, "_koff_written", {})
        gen["kinds_offered_dk"] = _ksorted(
            [list(dk_), k, list(ko), n - was_off.get((dk_, k, ko), 0)]
            for (dk_, k, ko), n in ag._kind_offered_dk.items()
            if n > was_off.get((dk_, k, ko), 0))
    if gamma._USED_CARRY:
        # L1b: Rank.used per unit since the last write; the load sums the chain (the reviewer
        # 2026-10-17 19:06, 19:33). Paid is not written here: 7i's replay restores it
        uu = ag.gamma.unit_weights()[0]
        was = getattr(ag, "_uu_written", {})
        gen["unit_used"] = {k: n - was.get(k, 0) for k, n in sorted(uu.items())
                            if n > was.get(k, 0)}
    if tether._7H_TRACE and hasattr(ag, "_line_grade"):
        # 7h (d): how each kind's lines ended since the last write; the load sums the chain
        gen["line_grades"] = {k: {o: n - ag._line_grade_written.get(k, {}).get(o, 0)
                                  for o, n in sorted(c.items())
                                  if n > ag._line_grade_written.get(k, {}).get(o, 0)}
                              for k, c in sorted(ag._line_grade.items())}
    if tether._M7_INV and hasattr(ag, "_inv_carry"):
        # M7-INV: the inventions made since the last write, as their method, with the standing
        # their term holds now (a record of it; the next game starts them on trial)
        gen["inventions"] = [{**r, "standing": ("settled" if ag.gamma.is_settled(r["term"])
                                                else "candidate")}
                             for r in ag._inv_carry[ag._inv_carry_written:]]
    if tether._7H_ROOT_GRADE and hasattr(ag, "_root_grade"):
        # 7h (a): the root shapes' outcome counts since the last write; the load sums the chain
        gen["root_grades"] = {s: {o: n - ag._root_grade_written.get(s, {}).get(o, 0)
                                  for o, n in sorted(c.items())
                                  if n > ag._root_grade_written.get(s, {}).get(o, 0)}
                              for s, c in sorted(ag._root_grade.items())}
    if tether._7H_KIND_CARRY and hasattr(ag, "_kind_n"):
        # 7h (h): A1's counts by kind since the last write; the load sums the chain
        gen["kind_counts"] = {site: {k: n - ag._kind_n_written[site].get(k, 0)
                                     for k, n in sorted(c.items())
                                     if n > ag._kind_n_written[site].get(k, 0)}
                              for site, c in ag._kind_n.items()}
    if tether._REACH_RANK and hasattr(ag, "_cause_kind_n"):
        # E1 part 2: which kind of object caused which kind of effect, since the last write
        gen["cause_kinds"] = {k: n - ag._cause_kind_written.get(k, 0)
                              for k, n in sorted(ag._cause_kind_n.items())
                              if n > ag._cause_kind_written.get(k, 0)}
    if tether._ENTRY_USE and hasattr(ag, "_entry_use"):
        # 1b: each library entry's use since the last write (counts as deltas; last explained)
        eu = {}
        for k, c in sorted(ag._entry_use.items()):
            w = ag._entry_use_written.get(k, {})
            d = {f: n - w.get(f, 0) for f, n in c.items() if f != "last" and n > w.get(f, 0)}
            if c.get("last") is not None and c.get("last") != w.get("last"):
                d["last"] = c["last"]
            if d:
                eu[k] = d
        gen["entry_use"] = eu
    if tether._3A_DIAGNOSE and hasattr(ag, "_3a_hazard"):
        # E2: the hazard by KIND and by ACTOR (templates, never a board's spots), since the last
        # write; the load adds them back as a head start. Pending unseen credits the agent's own
        # act reached are settled first, so a lineage never carries one (the reviewer 09:40)
        ag._3a_settle()
        gen["hazard_3a"] = {fam: {k: n - ag._3a_written.get(fam, {}).get(k, 0)
                                  for k, n in sorted(c.items())
                                  if n > ag._3a_written.get(fam, {}).get(k, 0)}
                            for fam, c in _hazard_families(ag._3a_hazard).items()}
    raw = _dumps(gen)
    h = hashlib.sha256(raw).hexdigest()[:16]
    try:
        with open(p / f"{PREFIX}{h}.json", "xb") as fh:
            fh.write(_store_bytes(raw))
    except FileExistsError:
        if store_con is not None:
            store_con.close()
        return {"refused": f"{PREFIX}{h}.json exists; a generation is never overwritten"}
    if _BOUNDARY:   # the next write in this instance extends THIS one: one line (F2)
        ag.lineage_parent = h
        ag._lineage_written = {**written, **{n: {"born": h, "handle": hd} for n, hd in new_names}}
        ag._lineage_marks = {"dormant": len(dormant_all), "evidence": len(ag.gamma.evidence)}
        if "kinds_landed" in gen:
            ag._kinds_carried = ag._kinds_carried | new_kinds
            ag._kind_episode_mark = len(ag._kind_episodes)
        if "kinds_landed_n" in gen:
            ag._kn_written = dict(ag._kind_landed_n)
        # a write without the boundary is a sibling of the last (the parent does not advance),
        # so the mark moves only with the parent
        if "unit_used" in gen:
            ag._uu_written = uu
        if "kinds_landed_dk" in gen:
            ag._kdk_written = dict(ag._kind_landed_dk)
            ag._koff_written = dict(ag._kind_offered_dk)
        if "line_grades" in gen:
            ag._line_grade_written = {k: dict(c) for k, c in ag._line_grade.items()}
        if "root_grades" in gen:
            ag._root_grade_written = {s: dict(c) for s, c in ag._root_grade.items()}
        if "inventions" in gen:
            ag._inv_carry_written = len(ag._inv_carry)
        if "kind_counts" in gen:
            ag._kind_n_written = {site: dict(c) for site, c in ag._kind_n.items()}
        if "cause_kinds" in gen:
            ag._cause_kind_written = dict(ag._cause_kind_n)
        if "hazard_3a" in gen:
            ag._3a_written = {f: dict(c) for f, c in _hazard_families(ag._3a_hazard).items()}
        if "entry_use" in gen:
            ag._entry_use_written = {k: dict(c) for k, c in ag._entry_use.items()}
    # D3: the index AFTER the generation; its failure is recorded and never costs the generation
    try:
        idx = write_index(p, ag, h)
    except Exception as e:  # noqa: BLE001 -- recorded in the report, never raised past here
        idx = {"failed": f"{type(e).__name__}: {e}"[:200]}
    try:   # the bound memo by name, after the index; the same never-costs-the-generation rule
        memo = write_memo(p, ag, h)
    except Exception as e:  # noqa: BLE001 -- recorded in the report, never raised past here
        memo = {"failed": f"{type(e).__name__}: {e}"[:200]}
    try:   # S1b: the slot answers, the same rule
        slot_memo = write_bs(p, ag, h)
    except Exception as e:  # noqa: BLE001 -- recorded in the report, never raised past here
        slot_memo = {"failed": f"{type(e).__name__}: {e}"[:200]}
    try:   # S1g: the asked record, the same rule
        asked = write_ak(p, ag, h)
    except Exception as e:  # noqa: BLE001 -- recorded in the report, never raised past here
        asked = {"failed": f"{type(e).__name__}: {e}"[:200]}
    store = None
    counts = {"terms": len(terms), "status": len(status), "evidence": len(gen["evidence"]),
              "dormant": len(dormant), "dormant_refused": len(refused)}
    if store_con is not None:
        # THE ORDER (the reviewer 07:12 item 4): the archive's files synced first, then the merge;
        # a crash between the two leaves the save unmerged, and the next open merges it
        import lineage_store as ls
        try:
            t0 = time.perf_counter()
            for f in sorted(p.glob(f"*{h}*.json")):
                _fsync(f)
            t_fsync = round(time.perf_counter() - t0, 3)
            # M2 (the reviewer 2026-10-19 19:21): the save is merged from its own bytes, as a
            # catch_up rebuild reads them; the dict built for them, and then the bytes, are let go
            # first, so they are not held through the merge
            gen = terms = status = dormant = refused = None
            g = json.loads(raw)
            raw = None
            store = ls.merge_save(store_con, p, h, g)
            g = None
            store["s_fsync"] = t_fsync
            if sleep:
                store["sleep"] = ls.sleep(store_con)
            elif ls.WAL_BOUND_BYTES is not None and ls.wal_bytes(p) > ls.WAL_BOUND_BYTES:
                # the WAL's SIZE bound (07:12 c, 07:19 3, 08:03 3b): a checkpoint at this boundary,
                # never mid-move; its time is a PLAY-PATH cost and is reported as one
                store["wal_bound"] = {"wal_bytes": ls.wal_bytes(p), **ls.checkpoint(store_con)}
        except ls.Refused as e:
            store = {"refused": str(e)[:200]}
        finally:
            store_con.close()
    return {"written": f"{PREFIX}{h}.json", "hash": h, "parent": parent, **counts,
            "index": idx, "memo": memo,
            "slot_memo": slot_memo, "asked": asked, **({"store": store} if store else {})}


def boundary(d: str | Path | None, ag: Any, game: str, how: str) -> dict | None:
    """THE BOUNDARY WRITE, one path for both runners (arc_holdout.play, tether_agent.run): a
    generation at a level clear ("level") or a terminal edge ("death", "game_win"), as write() makes
    one at the game's end. None unless the boundary arm, the carry and a folder are all present."""
    if not (_BOUNDARY and _CARRY and d):
        return None
    # agent_level: Agent.level, which counts WIN/death edges, and level clears too only under
    # TETHER_LEVEL_EDGE (F1); the 'how' field is the true label of the write
    return {"how": how, "agent_level": ag.level, **write(d, ag, game, sleep=False)}


def _heal(p: Path, ok: bool, why: str) -> tuple[bool, str, dict]:
    """H: a store failing its cheap check is checkpointed if it has a WAL and checked again, the
    size check AND a quick_check (a checkpoint can extend a short file over a page it lost); if it
    still fails, its files are renamed .dead-<UTC> (kept, never deleted) and the folder reads as one
    with no store, which open_store creates and catch_up rebuilds from the saves."""
    import sqlite3

    import lineage_store as ls
    rep: dict = {}
    if not ok and why != "no store" and ls.wal_bytes(p) > 0:
        rep["wal_bytes"] = ls.wal_bytes(p)
        qc = None
        try:
            con = ls.open_store(p)
            try:
                rep.update(ls.checkpoint(con))
                # a checkpoint can EXTEND a short file to the WAL's page count, and a cut page
                # the WAL does not hold then reads as zeros: the size check would pass on it.
                # Its own try: on a lost page quick_check can RAISE rather than report (h_chain2
                # f4), and that is not a failed checkpoint
                try:
                    qc = con.execute("PRAGMA quick_check").fetchone()[0]
                except sqlite3.DatabaseError as e:
                    qc = f"error: {e}"[:200]
            finally:
                con.close()
        except (sqlite3.DatabaseError, ls.Refused) as e:
            rep["checkpoint_failed"] = str(e)[:200]
        ok, why = ls.header_ok(p)
        rep["after_checkpoint"], rep["quick_check"] = why, qc
        if ok and qc != "ok":
            ok, why = False, f"quick_check {qc}"[:200]
    if not ok and why != "no store":
        stamp = time.strftime("%Y%m%dT%H%M%SZ", time.gmtime())
        moved, tries = [], {}
        for n in (ls.DB, f"{ls.DB}-wal", f"{ls.DB}-shm"):
            if not (p / n).exists():
                continue
            err = _rename_retry(p / n, p / f"{n}.dead-{stamp}", tries, n)
            if err is None:
                moved.append(n)
                continue
            # another process holds it past the schedule: put back what this call moved and refuse,
            # so _store_view raises Refused (the fallback before H) and the load never crashes
            for m in moved:
                (p / f"{m}.dead-{stamp}").rename(p / m)
            rep["set_aside_failed"] = {"why": why, "file": n, "error": err[:200], "attempts": tries,
                                       "restored": moved}
            return False, f"set-aside failed: {n} {err}"[:200], rep
        rep["set_aside"] = {"why": why, "files": moved, "suffix": f".dead-{stamp}",
                            "attempts": tries}
        ok, why = ls.header_ok(p)
    return ok, why, rep


# H's set-aside rename retries on a fixed schedule (the reviewer 2026-10-19 17:58 3b): an outside
# holder of the file (an antivirus scan, an indexer) is usually brief. 6 attempts, 2.0 s of waits
_RENAME_WAITS = (0.1, 0.2, 0.3, 0.6, 0.8)


def _rename_retry(src: Path, dst: Path, tries: dict, n: str) -> str | None:
    """None once src is renamed to dst, else the last error after the schedule. tries[n] counts the
    attempts made."""
    err = None
    for i, wait in enumerate((0.0, *_RENAME_WAITS)):
        if wait:
            time.sleep(wait)
        tries[n] = i + 1
        try:
            src.rename(dst)
            return None
        except OSError as e:
            err = f"{type(e).__name__}: {e}"
    return err


def _store_view(d: str | Path, ag: Any) -> dict:
    """Everything load() takes from the chain, read from the memory folder's store after merging
    any save it lacks. Reads only, so a refusal leaves the agent untouched."""
    import compile_term
    import lineage_store as ls
    p = Path(d)
    if any(p.glob(f"{BMEMO}*.json")) or any(p.glob(f"{BSMEMO}*.json")):
        raise ls.Refused("bm_/bs_ files are in the archive; the store does not hold them")
    ok, why = ls.header_ok(p)
    healed: dict = {}
    if _STORE_HEAL:
        ok, why, healed = _heal(p, ok, why)
    if not ok and why != "no store":
        raise ls.Refused(f"the store failed its check at open: {why}")
    con = ls.open_store(p)
    try:
        merged = ls.catch_up(con, p)
        sym = dict(con.execute("SELECT id, s FROM sym"))
        tip = con.execute("SELECT v FROM meta WHERE k='last_merged'").fetchone()
        if tip is None:     # a first-ever load: no save merged, no blob yet (the root view)
            return {"tip": None, "fold": None, "counts": None, "merged": merged, "healed": healed}
        f = json.loads(con.execute("SELECT v FROM blob WHERE k='fold'").fetchone()[0])
        c = json.loads(con.execute("SELECT v FROM blob WHERE k='counts'").fetchone()[0])
        atoms = {a.name: a for a in ag.gamma.atoms}
        sig = compile_term.signature(atoms)
        arm, parts = _sig_parts(sig)
        sigs = {i: (json.loads(a), json.loads(b)) for i, a, b in
                con.execute("SELECT id, arm, atoms FROM sig")}
        if any(a != arm or set(b) != set(parts) for a, b in sigs.values()):
            raise ls.Refused("a carried index was written under another signature")

        def key(*xs):
            return tuple(tuple(json.loads(sym[x])) if i in xs[0] else sym[x]
                         for i, x in enumerate(xs[1:]))
        # THE KIND TRIO IS NOT READ (the reviewer 08:17 item 2, 10:45): the pair table, the
        # known-with-no-count keys and the T2 candidates (two partial indexes), and two counters
        pairs = con.execute("SELECT kind_o, kind_x, n, last_seq FROM pair").fetchall()
        nocount = con.execute("SELECT entry, role, kind_o, kind_x FROM kind "
                              "WHERE has_n = 0 AND in_landed = 1").fetchall()
        t2 = con.execute("SELECT entry, role, kind_o, kind_x, n, has_n, l_game, l_level, "
                         "l_cycle, l_seq FROM kind WHERE no_dk = 1 AND in_landed = 1").fetchall()
        meta = dict(con.execute("SELECT k, v FROM meta WHERE k IN "
                                "('kinds_known', 'kind_seq_max')"))
        kdk = con.execute("SELECT dk, entry, tgt, n, l_game, l_level, l_cycle, l_seq "
                          "FROM kind_dk").fetchall()
        koff = con.execute("SELECT dk, entry, ko, n FROM kind_off").fetchall()
        held = con.execute("SELECT key, role, gen, items FROM held").fetchall()
        wholes = con.execute("SELECT entry, role, o, x FROM ak_whole").fetchall()
        # the O(life) parts from their append-only tables, in fold()'s chain order (schema 4)
        evidence = [json.loads(r) for (r,) in
                    con.execute("SELECT row FROM evidence ORDER BY k, i")]
        vindication = [json.loads(r) for (r,) in
                       con.execute("SELECT row FROM vindication ORDER BY k, i")]
        seeds = [json.loads(s_) for (s_,) in con.execute("SELECT seed FROM seeds ORDER BY k")]
    finally:
        con.close()
    return {"tip": tip and tip[0], "fold": f, "counts": c, "merged": merged, "healed": healed,
            "sig": sig,
            "atoms": atoms, "folder": str(p.resolve()),
            "evidence": evidence, "vindication": vindication, "seeds": seeds,
            "pairs": {(tuple(json.loads(sym[o])), tuple(json.loads(sym[x]))): (n, max(last, 0))
                      for o, x, n, last in pairs},
            "nocount": {key((2, 3), e, r, ko, kx) for e, r, ko, kx in nocount},
            "t2": {key((2, 3), e, r, ko, kx): (n if hn else 1, tuple(lv))
                   for e, r, ko, kx, n, hn, *lv in t2},
            "kinds_known": int(meta.get("kinds_known", 0)),
            "kind_seq_max": int(meta.get("kind_seq_max", 0)),
            "kdk": [(key((0, 2), dk, e, t), n, lv) for dk, e, t, n, *lv in kdk],
            "koff": [(key((0, 2), dk, e, ko), n) for dk, e, ko, n in koff],
            "held": [(sym[k], sym[r], g, json.loads(it)) for k, r, g, it in held],
            "wholes": wholes}


def _load_from_store(d: str | Path, ag: Any) -> dict:
    """load() under TETHER_MEMORY_STORE: the same agent state, built from the store. Each step
    mirrors load() below, in its order."""
    import tether
    v = _store_view(d, ag)
    h, f, c = v["tip"], v["fold"], v["counts"]
    ag.lineage_parent = h
    ag.gamma.keep_evidence = True
    if h is None:
        return {"parent": None, "root": "no generation yet; this instance writes the first"}
    if hasattr(ag, "_seed_from_lineage"):
        ag._seed_from_lineage(set(v["seeds"]), c["n_saves"], h)
    rep = ag.gamma.load_blob({"terms": list(f.get("rows", {}).values()),
                              "invented": f.get("invented", {}),
                              "vindication": v["vindication"],
                              "book": f.get("book", {})}, parent=h)
    rep["store_merged_at_load"] = len(v["merged"])
    if v["healed"]:
        rep["store_healed"] = v["healed"]
    if gamma._USED_CARRY:
        ag.gamma.carry_used(dict(c.get("unit_used", {})))
        rep["unit_used"] = len(c.get("unit_used", {}))
    if tether._7L_KIND and hasattr(ag, "_kind_known"):
        # the trio stays EMPTY: what its two readers need is held instead (tether _pair_counts,
        # _tiers' T2), as load-time snapshots, so a mid-game merge does not move them
        ag._kind_store = {"pairs": v["pairs"], "nocount": v["nocount"], "t2": v["t2"]}
        ag._kind_store_ver += 1
        ag._kind_pairs = ag._kind_pairs | set(v["pairs"])
        rep["kinds_known"] = v["kinds_known"]
        if tether._CONSOLIDATE:
            for k, _n, lv in v["kdk"]:
                if lv[0] is not None:
                    ag._kdk_last[k] = tuple(lv)
            ag._kind_seq = max(v["kind_seq_max"], ag._kind_seq)
            rep["kinds_set_form"] = c.get("kinds_set_form", 0)
    if tether._DELTA_KIND and hasattr(ag, "_kind_known_dk"):
        for k, n, _lv in v["kdk"]:
            if n:
                ag._kind_known_dk[k] += n
        for k, n in v["koff"]:
            ag._kind_known_off[k] += n
        rep["kinds_known_dk"] = len(ag._kind_known_dk)
        rep["kinds_known_off"] = len(ag._kind_known_off)
    if tether._7H_TRACE and hasattr(ag, "_line_grade_in"):
        for k, d_ in c.get("line_grades", {}).items():
            ag._line_grade_in.setdefault(k, {}).update(d_)
        rep["line_kinds_in"] = len(ag._line_grade_in)
    if tether._7H_ROOT_GRADE and hasattr(ag, "_root_grade_in"):
        for s, d_ in c.get("root_grades", {}).items():
            ag._root_grade_in.setdefault(s, {}).update(d_)
        rep["root_shapes_in"] = len(ag._root_grade_in)
    if tether._M7_INV and hasattr(ag, "_reinvent_carried"):
        rep["inventions_in"] = ag._reinvent_carried(list(c.get("inventions", [])))
    if tether._7H_KIND_CARRY and hasattr(ag, "_kind_carried_in"):
        for site, d_ in c.get("kind_counts", {}).items():
            ag._kind_carried_in.setdefault(site, {}).update(d_)
        rep["kind_counts_in"] = {s: sum(x.values()) for s, x in ag._kind_carried_in.items()}
    if tether._REACH_RANK and hasattr(ag, "_cause_kind_in"):
        ag._cause_kind_in.update(c.get("cause_kinds", {}))
        rep["cause_kinds_in"] = len(ag._cause_kind_in)
    if tether._ENTRY_USE and hasattr(ag, "_entry_use_in"):
        for ek, du in c.get("entry_use", {}).items():
            ag._entry_use_in.setdefault(ek, {}).update(du)
        rep["entry_use_in"] = len(ag._entry_use_in)
    if tether._3A_DIAGNOSE and hasattr(ag, "_3a_hazard"):
        fams = _hazard_families(ag._3a_hazard)
        for fam, d_ in c.get("hazard_3a", {}).items():
            if fam in fams:
                fams[fam].update(d_)
                ag._3a_in.setdefault(fam, {}).update(d_)
        ag._3a_written = {fm: dict(x) for fm, x in fams.items()}
        rep["hazard_3a_in"] = {fm: sum(x.values()) for fm, x in ag._3a_in.items()}
    if gamma._SETTLED_CORE:
        rep["replayed"] = ag.gamma.replay(v["evidence"])
    return {"parent": h, **rep, "index": _store_index(v), "memo": _store_none(v, "memo"),
            "slot_memo": _store_none(v, "bs"), "asked": _store_asked(v)}


def _store_index(v: dict) -> dict | None:
    """load_index's result from the store's held table (the tip's entry per key), one signature
    (anything else was refused in _store_view)."""
    import tether
    if not tether._INDEX_HOLD:
        return None
    known = _CARRIED.setdefault(v["folder"], set())
    n = 0
    for key, role, gh, items in v["held"]:
        k = (v["sig"], key, role)
        if k not in tether._INDEX_STORE:
            _PENDING[k] = {"gen": gh, "items": [(x["i"], x["ch"], _dec_c(x["c"], v["atoms"]),
                                                 _dec_c(x["t"], v["atoms"])) for x in items],
                           "folder": v["folder"]}
            n += 1
        known.add((repr(v["sig"]), key, role))
    return {"installed": n, "rekeyed": 0, "refusals_recompile": 0, "rebuild": [],
            "from_store": True}


def _store_none(v: dict, which: str) -> dict | None:
    """load_memo / load_bs with no bm_/bs_ files in the folder: the same known-set side effect."""
    import tether
    if which == "memo":
        if not (_CARRY and tether._INDEX_HOLD):
            return None
        _MEMO_CARRIED.setdefault(v["folder"], set())
    else:
        if not (_CARRY and tether._INDEX_HOLD and tether._SLOT_FILTER):
            return None
        _BS_CARRIED.setdefault(v["folder"], set())
    return {"pending": 0, "absent": v["counts"]["n_saves"], "signature_differs": 0,
            "unreadable": 0, "bytes": 0, "from_store": True}


def _store_asked(v: dict) -> dict | None:
    """load_ak's result from the store: only the WHOLE pairs pend (the slot rows carry no decision
    reader since E1 C4; the reviewer 04:36); the condensed tally stays on disk."""
    import tether
    if not (_CARRY and _RECORD and tether._INDEX_HOLD and tether._SLOT_FILTER):
        return None
    _AK_CARRIED.setdefault(v["folder"], set())
    for e, r, o, x in v["wholes"]:
        p_ = _AK_PENDING.setdefault((v["sig"], e, r, o, x),
                                    {"gen": v["tip"], "slots": set(), "folder": v["folder"]})
        p_["slots"].add(None)
    return {"pending": len(_AK_PENDING), "from_store": True}


def load(d: str | Path, ag: Any) -> dict:
    """The next instance's start: the chain folded into its Gamma as IMPORTED terms naming the tip,
    and the evidence record turned on. The fold's evidence and dormant record are not read back."""
    if _MEMORY_STORE and d:
        import lineage_store
        try:
            return _load_from_store(d, ag)
        except lineage_store.Refused as e:
            _c, _s, _lv = ag._boundary_key("@lineage")
            ag.led.record(_c, "IMPORT", _s, "store_refused", **_lv, reason=str(e)[:300],
                          reads="the memory store could not answer exactly; loaded from the saves")
    if _ONE_PASS:
        p = Path(d)
        chain = _chain(p) if p.is_dir() else []
        h, f = (chain[-1][0] if chain else None), fold(chain)
    else:
        h, f = head(d)
    ag.lineage_parent = h
    ag.gamma.keep_evidence = True
    if h is None:
        return {"parent": None, "root": "no generation yet; this instance writes the first"}
    if not _ONE_PASS:
        chain = _chain(Path(d))
    # the being's seed BEFORE anything is installed, so a handle the load mints is minted under
    # the seed a replay will read (F-a, the reviewer 2026-10-15 15:23)
    if hasattr(ag, "_seed_from_lineage"):
        ag._seed_from_lineage({g["seed"] for _, g in chain if g.get("seed")}, len(chain), h)
    rep = ag.gamma.load_blob({"terms": f["terms"], "invented": f["invented"],
                              "vindication": f["vindication"], "book": f["book"]}, parent=h)
    if gamma._USED_CARRY:
        # L1b: every generation's Rank.used per unit, root to tip, into the code
        tot: dict[str, int] = {}
        for _h, g in chain:
            for k, n in (g.get("unit_used") or {}).items():
                tot[k] = tot.get(k, 0) + n
        ag.gamma.carry_used(tot)
        rep["unit_used"] = len(tot)
    import tether
    if tether._7L_KIND and hasattr(ag, "_kind_known"):
        # 7l: every generation's kinds, root to tip, known to this instance (7m reads them)
        ag._kind_known = {(k, r, tuple(ko), tuple(kx)) for _h, g in chain
                          for k, r, ko, kx in g.get("kinds_landed", ())}
        ag._kind_pairs = ag._kind_pairs | {(ko, kx) for _k, _r, ko, kx in ag._kind_known}
        rep["kinds_known"] = len(ag._kind_known)
        if tether._CONSOLIDATE:
            # CONSOLIDATION: landings summed root to tip; a generation written before the counts
            # (set form) gives each of its keys n = 1, counted; the latest landing wins by seq
            set_form = 0
            for _h, g in chain:
                if "kinds_landed_n" in g:
                    for k, r, ko, kx, n in g["kinds_landed_n"]:
                        ag._kind_known_n[(k, r, tuple(ko), tuple(kx))] += n
                else:
                    for k, r, ko, kx in g.get("kinds_landed", ()):
                        ag._kind_known_n[(k, r, tuple(ko), tuple(kx))] += 1
                        set_form += 1
                for k, r, ko, kx, *v in g.get("kinds_last", ()):
                    e_ = (k, r, tuple(ko), tuple(kx))
                    if v[3] >= ag._kind_last.get(e_, (0, 0, 0, -1))[3]:
                        ag._kind_last[e_] = tuple(v)
                for d_, k, t_, *v in g.get("kinds_dk_last", ()):
                    e_ = (tuple(d_), k, tuple(t_))
                    if v[3] >= ag._kdk_last.get(e_, (0, 0, 0, -1))[3]:
                        ag._kdk_last[e_] = tuple(v)
            ag._kind_seq = max([v[3] for v in ag._kind_last.values()] + [ag._kind_seq])
            rep["kinds_set_form"] = set_form
    if tether._DELTA_KIND and hasattr(ag, "_kind_known_dk"):
        # K1: every generation's landings with their delta kind, root to tip
        for _h, g in chain:
            for dk_, k, tg, n in g.get("kinds_landed_dk", ()):
                ag._kind_known_dk[(tuple(dk_), k, tuple(tg))] += n
            for dk_, k, ko, n in g.get("kinds_offered_dk", ()):
                ag._kind_known_off[(tuple(dk_), k, tuple(ko))] += n
        rep["kinds_known_dk"] = len(ag._kind_known_dk)
        rep["kinds_known_off"] = len(ag._kind_known_off)
    if tether._7H_TRACE and hasattr(ag, "_line_grade_in"):
        # 7h (d): every generation's line grades, root to tip
        for _h, g in chain:
            for k, c in g.get("line_grades", {}).items():
                into = ag._line_grade_in.setdefault(k, {})
                for o, n in c.items():
                    into[o] = into.get(o, 0) + n
        rep["line_kinds_in"] = len(ag._line_grade_in)
    if tether._7H_ROOT_GRADE and hasattr(ag, "_root_grade_in"):
        # 7h (a): every generation's root grades, root to tip
        for _h, g in chain:
            for s, c in g.get("root_grades", {}).items():
                into = ag._root_grade_in.setdefault(s, {})
                for o, n in c.items():
                    into[o] = into.get(o, 0) + n
        rep["root_shapes_in"] = len(ag._root_grade_in)
    if tether._M7_INV and hasattr(ag, "_reinvent_carried"):
        # M7-INV: every generation's inventions, root to tip, re-invented on trial
        rep["inventions_in"] = ag._reinvent_carried(
            [r for _h, g in chain for r in g.get("inventions", ())])
    if tether._7H_KIND_CARRY and hasattr(ag, "_kind_carried_in"):
        # 7h (h): the kind counts of every generation, root to tip, read as A1's second key
        for _h, g in chain:
            for site, c in g.get("kind_counts", {}).items():
                into = ag._kind_carried_in.setdefault(site, {})
                for k, n in c.items():
                    into[k] = into.get(k, 0) + n
        rep["kind_counts_in"] = {s: sum(c.values()) for s, c in ag._kind_carried_in.items()}
    if tether._REACH_RANK and hasattr(ag, "_cause_kind_in"):
        # E1 part 2: the cause-kind record of every generation, root to tip, read by the boost
        for _h, g in chain:
            for k, n in g.get("cause_kinds", {}).items():
                ag._cause_kind_in[k] = ag._cause_kind_in.get(k, 0) + n
        rep["cause_kinds_in"] = len(ag._cause_kind_in)
    if tether._ENTRY_USE and hasattr(ag, "_entry_use_in"):
        # 1b: every generation's entry use, root to tip, summed (last: the latest stamp)
        for _h, g in chain:
            for ek, du in g.get("entry_use", {}).items():
                into = ag._entry_use_in.setdefault(ek, {})
                for fld, n in du.items():
                    into[fld] = n if fld == "last" else into.get(fld, 0) + n
        rep["entry_use_in"] = len(ag._entry_use_in)
    if tether._3A_DIAGNOSE and hasattr(ag, "_3a_hazard"):
        # E2: every generation's kind/actor hazard, root to tip, added to this agent's own
        fams = _hazard_families(ag._3a_hazard)
        for _h, g in chain:
            for fam, c in g.get("hazard_3a", {}).items():
                if fam in fams:
                    fams[fam].update(c)
                    into = ag._3a_in.setdefault(fam, {})
                    for k, n in c.items():
                        into[k] = into.get(k, 0) + n
        ag._3a_written = {f: dict(c) for f, c in fams.items()}   # carried-in is not re-written
        rep["hazard_3a_in"] = {f: sum(c.values()) for f, c in ag._3a_in.items()}
    if gamma._SETTLED_CORE:
        # 7i (2): a carried term keeps the standing it had, LEARNED and revisable (the reviewer
        # 2026-10-15 19:04); the record itself is unchanged
        rep["replayed"] = ag.gamma.replay(f["evidence"])
    return {"parent": h, **rep, "index": load_index(d, ag, chain),
            "memo": load_memo(d, ag, chain), "slot_memo": load_bs(d, ag, chain),
            "asked": load_ak(d, ag, chain)}


def merge(d: str | Path, tips: list[str] | None = None) -> dict:
    """Join branches: one MERGE generation naming every given tip (default: all of them) as its
    parents and holding nothing else. No tip is picked and nothing is copied or removed; the fold
    reads both branches (Fig 9). Named by its own hash, opened "xb", never overwritten."""
    p = Path(d)
    gens = _read(p)
    now = _tips(gens)
    tips = sorted(set(now if tips is None else tips))
    if not set(tips) <= set(now):
        raise ValueError(f"lineage.merge: not current tips: {sorted(set(tips) - set(now))}")
    if len(tips) < 2:
        return {"refused": "nothing to merge", "tips": tips}
    gen = {"lineage": 1, "parents": tips, "merge": True, "game": None, "terms": [], "status": [],
           "evidence": [], "vindication_tail": [], "book": {}, "invented": {}, "dormant": [],
           "dormant_refused": []}
    raw = _dumps(gen)
    h = hashlib.sha256(raw).hexdigest()[:16]
    try:
        with open(p / f"{PREFIX}{h}.json", "xb") as fh:
            fh.write(_store_bytes(raw))
    except FileExistsError:
        return {"refused": f"{PREFIX}{h}.json exists; a generation is never overwritten"}
    return {"written": f"{PREFIX}{h}.json", "hash": h, "parents": tips}


# -- D3: THE HELD INDEX, CARRIED BESIDE THE GENERATION (the reviewer 2026-10-14 21:59) -------------
# Under BOTH arms (_CARRY and tether's _INDEX_HOLD), each generation gets an index file beside it
# holding the held compiles THIS instance made, so a later instance installs them instead of
# compiling again (Fig 12 :107-108). The index is derived reach (Fig 6): it never moves the
# generation's hash, is never silently trusted, and a failure to write it never costs the
# generation (written first).
IDX = "idx_"
_CARRIED: dict[str, set] = {}   # lineage folder -> (signature repr, entry, role) in its index files
# carried references not yet asked for: (signature, entry, role) -> {gen, items}; resolved at the
# FIRST ask (resolve), never at load (the reviewer 22:27)
_PENDING: dict[tuple, dict] = {}
_RESOLVE: dict[str, int] = {"resolved": 0, "unresolved": 0}
_ROWED: set = set()   # generations that already wrote their one unresolved row


def _ch(cand: dict) -> str:
    """A candidate's content hash: the reference checks the library's own view against it."""
    return hashlib.sha256(json.dumps(enc(cand), sort_keys=True).encode("utf-8")).hexdigest()[:16]


# S1e (the reviewer 2026-10-15 13:01): a HELD candidate's hash, computed once. tether._INDEX_STORE
# sets the held view for (signature, entry, role) once and never rebuilds it in a process, so the
# candidate at position i under one signature is one object for the process, and a new signature
# is a new key. The object is kept beside its hash and checked by identity before reuse. The
# whole-check is unchanged: the same hashes, compared the same way. resolve()'s check of the LIVE
# library view does not use this: it exists to see a changed library, and runs once per key.
_CH_HELD: dict[tuple, tuple] = {}   # (signature, entry, role, position) -> (candidate, hash)


def _held_ch(sig: tuple, key: str, role: str, i: int, cand: dict) -> str:
    """_ch of a held candidate, once per (signature, entry, role, position) and object."""
    got = _CH_HELD.get((sig, key, role, i))
    if got is None or got[0] is not cand:
        got = _CH_HELD[(sig, key, role, i)] = (cand, _ch(cand))
    return got[1]


def _sig_parts(sig: tuple) -> tuple[Any, list]:
    """The relation arm and each template atom's tuple, as text (compile_term.signature)."""
    return sig[0], sorted(repr(a) for a in sig[1])


def _enc_term(t: Any) -> dict:
    return {"atoms": [a.name for a in t.atoms], "origin": t.origin, "operand": t.operand,
            "guard": t.guard, "guard_ref": t.guard_ref,
            "operand_term": _enc_term(t.operand_term) if t.operand_term is not None else None}


def _dec_term(x: dict, atoms: dict) -> Any:
    return gamma.Term(tuple(atoms[n] for n in x["atoms"]), origin=x["origin"],
                      operand=x["operand"], guard=x["guard"], guard_ref=x["guard_ref"],
                      operand_term=(_dec_term(x["operand_term"], atoms)
                                    if x["operand_term"] is not None else None))


def _enc_c(c: Any) -> Any:
    import compile_term
    if c is None:
        return None
    if isinstance(c, compile_term.Refusal):
        return {"refusal": c.reason}
    if isinstance(c, compile_term.Compiled):
        return {"slot": c.slot, "term": _enc_term(c.term), "operand": c.operand,
                "parties": list(c.parties), "absent": enc(c.absent),
                **({"via": c.via} if c.via else {})}
    raise Unencodable(type(c).__name__)


def _dec_c(x: Any, atoms: dict) -> Any:
    import compile_term
    if x is None:
        return None
    if "refusal" in x:
        return compile_term.Refusal(x["refusal"])
    return compile_term.Compiled(x["slot"], _dec_term(x["term"], atoms), x["operand"],
                                 tuple(x["parties"]), dec(x["absent"]), x.get("via"))


def write_index(d: str | Path, ag: Any, h: str) -> dict | None:
    """Beside generation `h`: the held compiles for this Gamma's signature that no index of this
    chain already holds (the extension, never a copy). Opened "xb", named by its own hash."""
    import compile_term
    import tether
    if not tether._INDEX_HOLD:
        return None
    p = Path(d)
    sig = compile_term.signature({a.name: a for a in ag.gamma.atoms})
    known = _CARRIED.setdefault(str(p.resolve()), set())
    entries, refused = [], []
    for (s, key, role), held in tether._INDEX_STORE.items():
        if s != sig or (repr(s), key, role) in known:
            continue
        try:
            # BY REFERENCE (the reviewer 22:22): the candidate is its position in the view and its
            # hash, never a copy of the library; the compile is the derived part, kept whole
            entries.append({"key": key, "role": role,
                            "items": [{"i": i, "ch": _held_ch(s, key, role, i, cand),
                                       "c": _enc_c(c), "t": _enc_c(t)}
                                      for i, (cand, c, t) in enumerate(held)]})
        except Unencodable as e:
            refused.append({"key": key, "role": role, "type": e.type})
    arm, parts = _sig_parts(sig)
    raw = _dumps({"gen": h, "sig_arm": arm, "sig_atoms": parts,
                  "sig_names": sorted(a[0] for a in sig[1]), "entries": entries,
                  "refused": refused})
    ih = hashlib.sha256(raw).hexdigest()[:16]
    name = f"{IDX}{h}_{ih}.json"
    try:
        with open(p / name, "xb") as fh:
            fh.write(_store_bytes(raw))
    except FileExistsError:
        return {"refused": f"{name} exists; an index is never overwritten"}
    known.update((repr(sig), e["key"], e["role"]) for e in entries)
    return {"written": name, "entries": len(entries), "refused": len(refused)}


def load_index(d: str | Path, ag: Any, chain: list) -> dict | None:
    """Each generation's index, root to tip, as references PENDING their first ask (resolve), never
    into tether's held store at load. EQUAL signature: installed.
    ADDITIONS ONLY (same arm, every old atom tuple present unchanged): re-keyed, except an entry
    holding a Refusal, which recompiles (an added atom may let it compile). Anything else -- a
    missing, unreadable or mismatched file, or another signature difference -- installs NOTHING
    from that file and writes one "index_rebuild" row naming the reason."""
    import compile_term
    import tether
    if not tether._INDEX_HOLD or not chain:
        return None
    p = Path(d)
    atoms = {a.name: a for a in ag.gamma.atoms}
    sig = compile_term.signature(atoms)
    arm, parts = _sig_parts(sig)
    known = _CARRIED.setdefault(str(p.resolve()), set())
    rep: dict = {"installed": 0, "rekeyed": 0, "refusals_recompile": 0, "rebuild": [], "bytes": 0}
    folder = str(p.resolve())
    counted: dict = {}   # key -> "installed" | "rekeyed", from the latest generation holding it
    for gh, _g in chain:
        if _g.get("merge"):
            continue      # a merge generation holds only the join: no compiles, so no index
        files = sorted(p.glob(f"{IDX}{gh}_*.json"))
        reason, body, same = None, None, False
        if len(files) != 1:
            reason = "missing" if not files else f"{len(files)} index files"
        else:
            import lineage_store as ls
            raw = ls.file_bytes(files[0])
            rep["bytes"] += len(raw)
            if files[0].stem != f"{IDX}{gh}_{hashlib.sha256(raw).hexdigest()[:16]}":
                reason = "hash mismatch"
            else:
                try:
                    body = json.loads(raw)
                except ValueError:
                    reason = "unreadable"
        if body is not None:
            old = set(body["sig_atoms"])
            same = body["sig_arm"] == arm and old == set(parts)
            # the one compile that reads the wider atom set (compile_term 236): an added CONVERSE
            # atom switches a template, so a compile that SUCCEEDED may differ; nothing re-keys
            conv = {n for row in compile_term.CONVERSE.values() for n in row[0]}
            added = {a[0] for a in sig[1]} - set(body.get("sig_names", []))
            if not same and not (body["sig_arm"] == arm and old < set(parts)):
                reason = (f"signature: arm {body['sig_arm']} -> {arm}; "
                          f"{len(old - set(parts))} atom(s) removed or changed")
            elif not same and added & conv:
                reason = ("an added atom changes a template choice (compile_term 236): "
                          f"{sorted(added & conv)}")
        if reason is not None:
            _c, _s, _lv = ag._boundary_key("@lineage")
            ag.led.record(_c, "IMPORT", _s, "index_rebuild", **_lv, generation=gh, reason=reason,
                          reads="nothing installed from this index; compiled as at HEAD")
            rep["rebuild"].append({"generation": gh, "reason": reason})
            continue
        for e in body["entries"]:
            items = [(x["i"], x["ch"], _dec_c(x["c"], atoms), _dec_c(x["t"], atoms))
                     for x in e["items"]]
            k = (sig, e["key"], e["role"])
            if not same and any(isinstance(z, compile_term.Refusal)
                                for _, _, b, c in items for z in (b, c)):
                rep["refusals_recompile"] += 1
                if k in counted:   # an earlier generation's entry for this key is older still
                    _PENDING.pop(k, None)
                    del counted[k]
                continue
            # THE TIP WINS (the reviewer 23:23): a later generation holds a key again only when
            # an earlier one missed and was rewritten (resolve), so it replaces the earlier entry
            if k not in tether._INDEX_STORE:
                _PENDING[k] = {"gen": gh, "items": items, "folder": folder}
                counted[k] = "installed" if same else "rekeyed"
            known.add((repr(sig), e["key"], e["role"]))
    for how in counted.values():
        rep[how] += 1
    return rep


def resolve(ag: Any, lib: Any, key: str, role: str, sig: tuple) -> list | None:
    """A carried reference at its FIRST ask (tether._held_index, both arms): the library's own view
    under the placeholders, checked WHOLE -- the same length and every position's hash. All match:
    the carried compiles are held and nothing is compiled. Any miss: the entry is dropped for this
    instance and compiled fresh, counted, and its generation writes one index_rebuild row; the
    fresh compile is written by this generation's index, so the key heals."""
    import tether
    p = _PENDING.pop((sig, key, role), None)
    if p is None:
        return None
    view = lib.view(key, role, tether.PH_O, tether.PH_X)
    items = p["items"]
    try:
        match = len(view) == len(items) and all(i < len(view) and _ch(view[i]) == ch
                                                for i, ch, _, _ in items)
    except Unencodable:   # a view candidate with no form is a MISS, never raised to the agent
        match = False
    if match:
        held = [(view[i], c, t) for i, _, c, t in items]
        tether._INDEX_STORE[(sig, key, role)] = held
        for i, ch, _, _ in items:   # S1e: these candidates are now the held view, hash checked
            _CH_HELD[(sig, key, role, i)] = (view[i], ch)
        _RESOLVE["resolved"] += 1
        return held
    _RESOLVE["unresolved"] += 1
    # HEALS (the reviewer 23:23): the key leaves this folder's known set, so this generation's
    # write_index writes the fresh compile and the next load takes it (the tip wins)
    _CARRIED.get(p["folder"], set()).discard((repr(sig), key, role))
    if p["gen"] not in _ROWED:
        _ROWED.add(p["gen"])
        _c, _s, _lv = ag._boundary_key("@lineage")
        ag.led.record(_c, "IMPORT", _s, "index_rebuild", **_lv, generation=p["gen"],
                      reason="unresolved candidates: the library's view no longer matches",
                      reads="the entry compiled fresh; the carried compile was not used")
    return None


# -- THE BOUND MEMO, CARRIED BY NAME BESIDE THE GENERATION (the reviewer 2026-10-15 06:10, 06:13,
# 06:56, 07:00; Isaiah 06:01) -------------------------------------------------------------------
# Under BOTH arms (_CARRY and tether's _INDEX_HOLD) each generation gets a memo file holding the
# bound answers THIS instance made that no earlier file of the chain holds. Objects never cross a
# process: each answer is written by atom NAME (_enc_c) and its candidate by position and hash
# (_ch), and at the first ask it is bound onto THIS Gamma's code primitives (_dec_c), checked
# whole against the held view, as resolve does. A miss binds fresh and heals at the next write.
# Write point: the generation (game end today); loss window: the current game.
BMEMO = "bm_"
_MEMO_CARRIED: dict[str, set] = {}   # folder -> (signature repr, entry, role, o, x) in its files
_MEMO_PENDING: dict[tuple, dict] = {}   # (signature, entry, role, o, x) -> {gen, items, folder}
_MEMO_RESOLVE: dict[str, int] = {"resolved": 0, "unresolved": 0}


def _memo_source(ag: Any) -> list:
    """(sig, entry, role, o, x, answers) this instance can see: the process memo's rows for its
    token, or its own per-Agent memo."""
    import tether
    tok = getattr(ag, "_atoms_token", None)
    if tok:
        return [(k[1], k[2], k[3], k[4], k[5], v) for k, v in tether._BOUND_MEMO.items()
                if k[0] == tok]
    return [(k[1], k[2], k[3], k[4], k[5], v) for k, v in ag._bound_cache.items()]


def _put_memo(p: Path, h: str, prefix: str, sig: tuple, entries: list, refused: list) -> dict:
    """One memo file beside generation `h`, opened "xb", named by its own hash."""
    arm, parts = _sig_parts(sig)
    raw = _dumps({"gen": h, "sig_arm": arm, "sig_atoms": parts, "entries": entries,
                  "refused": refused})
    name = f"{prefix}{h}_{hashlib.sha256(raw).hexdigest()[:16]}.json"
    try:
        with open(p / name, "xb") as fh:
            fh.write(_store_bytes(raw))
    except FileExistsError:
        return {"refused": f"{name} exists; a memo file is never overwritten"}
    return {"written": name, "entries": len(entries), "refused": len(refused)}


def _memo_bodies(p: Path, prefix: str, sig: tuple, chain: list, rep: dict,
                 any_sig: bool = False) -> Any:
    """Each generation's memo files of one family, root to tip: the body of every file whose name
    is its own hash and whose signature is EQUAL; every other file is counted, never read on.
    any_sig (S1g R1, the asked record): a file of another signature is counted AND read on, since
    a question stays true when the atoms change; its answer is rebuilt under the current one."""
    arm, parts = _sig_parts(sig)
    for gh, _g in chain:
        if _g.get("merge"):
            continue
        files = sorted(p.glob(f"{prefix}{gh}_*.json"))
        if not files:
            rep["absent"] += 1      # a generation written before the memo carried, or with none
            continue
        for f in files:
            import lineage_store as ls
            raw = ls.file_bytes(f)
            rep["bytes"] += len(raw)
            try:
                body = json.loads(raw)
            except ValueError:
                rep["unreadable"] += 1
                continue
            if f.stem != f"{prefix}{gh}_{hashlib.sha256(raw).hexdigest()[:16]}":
                rep["unreadable"] += 1
                continue
            if body["sig_arm"] != arm or set(body["sig_atoms"]) != set(parts):
                rep["signature_differs"] += 1
                if not any_sig:
                    continue
            yield gh, body


def write_memo(d: str | Path, ag: Any, h: str) -> dict | None:
    """Beside generation `h`: the bound answers for this Gamma's signature that no memo file of
    this chain already holds (the extension, never a copy). Opened "xb", named by its own hash."""
    import compile_term
    import tether
    if not (_CARRY and tether._INDEX_HOLD):
        return None
    if _RECORD and tether._SLOT_FILTER:   # S1g: the asked record carries these pairs
        return None
    p = Path(d)
    sig = compile_term.signature({a.name: a for a in ag.gamma.atoms})
    known = _MEMO_CARRIED.setdefault(str(p.resolve()), set())
    entries, refused = [], []
    for s, key, role, o, x, answers in _memo_source(ag):
        if s != sig or (repr(s), key, role, o, x) in known:
            continue
        try:
            entries.append({"key": key, "role": role, "o": o, "x": x,
                            "items": [{"i": i, "ch": _held_ch(s, key, role, i, cand),
                                       "c": _enc_c(c), "t": _enc_c(t)}
                                      for i, (cand, c, t) in enumerate(answers)]})
        except Unencodable as e:
            refused.append({"key": key, "role": role, "o": o, "x": x, "type": e.type})
    out = _put_memo(p, h, BMEMO, sig, entries, refused)
    if "written" in out:
        known.update((repr(sig), e["key"], e["role"], e["o"], e["x"]) for e in entries)
    return out


def load_memo(d: str | Path, ag: Any, chain: list) -> dict | None:
    """Each generation's memo file, root to tip, PENDING its first ask (resolve_memo). Only an
    EQUAL signature is taken; any other file installs nothing and is counted (a bound answer
    reads the compile it came from, so a changed signature means a different answer)."""
    import compile_term
    import tether
    if not (_CARRY and tether._INDEX_HOLD) or not chain:
        return None
    p = Path(d)
    sig = compile_term.signature({a.name: a for a in ag.gamma.atoms})
    folder = str(p.resolve())   # once per load, never per entry (the 13:25 install read)
    known = _MEMO_CARRIED.setdefault(folder, set())
    rep: dict = {"pending": 0, "absent": 0, "signature_differs": 0, "unreadable": 0, "bytes": 0}
    for gh, body in _memo_bodies(p, BMEMO, sig, chain, rep):
        for e in body["entries"]:
            k = (sig, e["key"], e["role"], e["o"], e["x"])
            _MEMO_PENDING[k] = {"gen": gh, "items": e["items"], "folder": folder}
            known.add((repr(sig), e["key"], e["role"], e["o"], e["x"]))
    rep["pending"] = len(_MEMO_PENDING)
    return rep


def resolve_memo(ag: Any, lib: Any, mkey: tuple, atoms: dict) -> tuple | None:
    """A carried bound answer at its FIRST ask (tether._compiled's bound path): the held view for
    the entry, checked WHOLE -- the same length and every position's hash -- then each answer
    bound onto THIS Gamma's code primitives by name. Any miss returns None (the caller binds
    fresh), is counted, and leaves the key out of the carried set, so the next write heals it."""
    _tok, sig, key, role, o, x = mkey
    p = _MEMO_PENDING.pop((sig, key, role, o, x), None)
    if p is None:
        return None
    try:
        held = ag._held_index(lib, key, role, atoms, sig)
        items = p["items"]
        if len(held) != len(items) or any(
                it["i"] >= len(held)
                or _held_ch(sig, key, role, it["i"], held[it["i"]][0]) != it["ch"]
                for it in items):
            raise LookupError("the held view no longer matches")
        got = tuple((held[it["i"]][0], _dec_c(it["c"], atoms), _dec_c(it["t"], atoms))
                    for it in items)
    except (LookupError, Unencodable):   # a name this Gamma lacks is a KeyError: a miss
        _MEMO_RESOLVE["unresolved"] += 1
        _MEMO_CARRIED.get(p["folder"], set()).discard((repr(sig), key, role, o, x))
        return None
    _MEMO_RESOLVE["resolved"] += 1
    return got


# S1b, THE SLOT ANSWERS CARRIED (the reviewer 2026-10-15 11:05, 11:22). Under TETHER_SLOT_FILTER the
# agent binds only the held rows that land on the asked slot (tether._lands), and those answers are
# what it learns in play, so they cross the boundary in their own family beside bm_, never written
# as a whole view. Each item is the HELD INDEX, its candidate's hash and the answer by atom name. At
# the first ask the held view's rows for that slot must be the SAME rows (the indices _lands keeps
# now equal the carried ones, every hash equal): WHOLE FOR THAT SLOT. Any miss binds fresh, is
# counted, and heals at the next write. Write point and loss window: bm_'s.
BSMEMO = "bs_"
# folder -> (signature repr, entry, role, o, x, slot) in its files
_BS_CARRIED: dict[str, set] = {}
_BS_PENDING: dict[tuple, dict] = {}   # (signature, entry, role, o, x, slot) -> {gen, items, folder}
_BS_RESOLVE: dict[str, int] = {"resolved": 0, "unresolved": 0}


def _bs_source(ag: Any) -> list:
    """((sig, entry, role, o, x, slot), held indices, answers) this instance can see, for pairs with
    NO whole in the whole memo: S1d (the reviewer 2026-10-15 12:42). A promoted pair is carried
    once, as its whole, by bm_, and every slot of it is served from that whole's slot map, so a
    slot answer cut from it is authored from the whole and never carried again."""
    import tether
    tok = getattr(ag, "_atoms_token", None)
    memo = tether._BOUND_SLOT_MEMO if tok else ag._bound_slot_cache
    idx = tether._BOUND_SLOT_IDX if tok else ag._bound_slot_idx
    whole = tether._BOUND_MEMO if tok else ag._bound_cache
    return [(k[1:], idx[k], v) for k, v in memo.items()
            if k[0] == tok and k in idx and k[:6] not in whole]


def write_bs(d: str | Path, ag: Any, h: str) -> dict | None:
    """Beside generation `h`: the slot answers for this signature no bs_ file of the chain holds."""
    import compile_term
    import tether
    if not (_CARRY and tether._INDEX_HOLD and tether._SLOT_FILTER):
        return None
    if _RECORD:   # S1g: the asked record carries these pairs
        return None
    p = Path(d)
    sig = compile_term.signature({a.name: a for a in ag.gamma.atoms})
    known = _BS_CARRIED.setdefault(str(p.resolve()), set())
    entries, refused = [], []
    for (s, key, role, o, x, slot), idx, answers in _bs_source(ag):
        if s != sig or (repr(s), key, role, o, x, slot) in known:
            continue
        try:
            entries.append({"key": key, "role": role, "o": o, "x": x, "slot": slot,
                            "items": [{"i": i, "ch": _held_ch(s, key, role, i, cand),
                                       "c": _enc_c(c), "t": _enc_c(t)}
                                      for i, (cand, c, t) in zip(idx, answers, strict=True)]})
        except Unencodable as e:
            refused.append({"key": key, "role": role, "o": o, "x": x, "slot": slot,
                            "type": e.type})
    out = _put_memo(p, h, BSMEMO, sig, entries, refused)
    if "written" in out:
        known.update((repr(sig), e["key"], e["role"], e["o"], e["x"], e["slot"])
                     for e in entries)
    return out


def load_bs(d: str | Path, ag: Any, chain: list) -> dict | None:
    """Each generation's bs_ files, root to tip, PENDING their first ask (resolve_bs)."""
    import compile_term
    import tether
    if not (_CARRY and tether._INDEX_HOLD and tether._SLOT_FILTER) or not chain:
        return None
    p = Path(d)
    sig = compile_term.signature({a.name: a for a in ag.gamma.atoms})
    folder = str(p.resolve())   # once per load, never per entry (the 13:25 install read)
    known = _BS_CARRIED.setdefault(folder, set())
    rep: dict = {"pending": 0, "absent": 0, "signature_differs": 0, "unreadable": 0, "bytes": 0}
    for gh, body in _memo_bodies(p, BSMEMO, sig, chain, rep):
        for e in body["entries"]:
            k = (sig, e["key"], e["role"], e["o"], e["x"], e["slot"])
            _BS_PENDING[k] = {"gen": gh, "items": e["items"], "folder": folder}
            known.add((repr(sig), e["key"], e["role"], e["o"], e["x"], e["slot"]))
    rep["pending"] = len(_BS_PENDING)
    return rep


def resolve_bs(ag: Any, lib: Any, skey: tuple, atoms: dict) -> tuple | None:
    """(held indices, answers) for a carried slot answer at its FIRST ask, checked WHOLE FOR THAT
    SLOT, or None (the caller reads on, and binds fresh at the end)."""
    from functools import partial

    import tether
    _tok, sig, key, role, o, x, slot = skey
    p = _BS_PENDING.pop((sig, key, role, o, x, slot), None)
    if p is None:
        return None
    try:
        held = ag._held_index(lib, key, role, atoms, sig)
        sub = partial(tether._ph_sub, o=o, x=x)
        kept = [i for i, (_c, a, b) in enumerate(held) if tether._lands(role, a, b, slot, sub)
                and not (tether._SPEED2_COUNT
                         and tether._tally_key(role, a, b, sub) is not None)]
        items = p["items"]
        if kept != [it["i"] for it in items] or any(
                _held_ch(sig, key, role, it["i"], held[it["i"]][0]) != it["ch"] for it in items):
            raise LookupError("the held rows for this slot no longer match")
        got = tuple((held[it["i"]][0], _dec_c(it["c"], atoms), _dec_c(it["t"], atoms))
                    for it in items)
    except (LookupError, Unencodable):   # a name this Gamma lacks is a KeyError: a miss
        _BS_RESOLVE["unresolved"] += 1
        _BS_CARRIED.get(p["folder"], set()).discard((repr(sig), key, role, o, x, slot))
        return None
    _BS_RESOLVE["resolved"] += 1
    return tuple(kept), got


# S1g, THE ASKED RECORD's family. Each entry names a question this instance answered: a pair
# (entry, role, o, x) held as a WHOLE (slot None: it was reused, so the next process binds its whole
# at once), or a pair answered for ONE slot (that slot: the next process takes the first-slot path,
# as it would cold). The answers are never written; they are rebuilt from the carried index, which
# is checked against the live library at its first ask (resolve). Written once per generation for
# what the chain does not yet hold; never deleted, never rewritten.
AKMEMO = "ak_"
_AK_CARRIED: dict[str, set] = {}   # folder -> (entry, role, o, x, slot): no signature (R1)
_AK_PENDING: dict[tuple, dict] = {}   # (signature, entry, role, o, x) -> {gen, slots, folder}
_AK_N: dict[str, int] = {"whole": 0, "slot": 0}   # recorded pairs met at their first ask


def _ak_source(ag: Any, kept: bool = True) -> list:
    """((sig, entry, role, o, x), slot or None) for every question this instance answered --
    with, under CONSOLIDATION, the questions a fold already cleared from the stores (kept)."""
    import tether
    tok = getattr(ag, "_atoms_token", None)
    whole = tether._BOUND_MEMO if tok else ag._bound_cache
    smemo = tether._BOUND_SLOT_MEMO if tok else ag._bound_slot_cache
    out = [(k[1:], None) for k in whole if k[0] == tok]
    out += [(k[1:6], k[6]) for k in smemo if k[0] == tok and k[:6] not in whole]
    if kept and getattr(ag, "_ak_kept", None):
        have = set(out)
        out += [k for k in sorted(ag._ak_kept, key=repr) if k not in have]
    return out


def _ak_rows(ag: Any) -> Counter:
    """S4: the times-asked counter (Agent._ak_asked) keyed as _ak_source keys its rows -- a slot
    ask of a pair held WHOLE is that pair's whole row (slot None), as the old form writes it."""
    import tether
    tok = getattr(ag, "_atoms_token", None)
    whole = tether._BOUND_MEMO if tok else ag._bound_cache
    out: Counter = Counter()
    for k, n in ag._ak_asked.items():
        out[k[:6] + (None,) if k[:6] in whole else k] += n
    return out


def _ak_order(r: tuple) -> tuple:
    """Form 2's row order: the row's own fields, slot None after any slot (no repr, no sig)."""
    return r[0], r[1], r[2], r[3], r[4] is None, r[4] or ""


def _ak_entries(ag: Any, tok: Any, sig: tuple) -> Any:
    """Form 2's rows, in _ak_order, one dict at a time: (key, role, o, x, slot) of this token and
    signature from the times-asked counter, a slot ask of a pair held WHOLE folded into that
    pair's whole row (its n summed, as _ak_rows sums it). One sorted list of row tuples is held,
    never a copy of the counter nor the file's encoded form."""
    import tether
    whole = tether._BOUND_MEMO if tok else ag._bound_cache
    rows = sorted(((k[2:6] + (None,) if k[:6] in whole else k[2:], n)
                   for k, n in ag._ak_asked.items()
                   if k[0] == tok and (k[1] is sig or k[1] == sig)),
                  key=lambda rn: _ak_order(rn[0]))
    i = 0
    while i < len(rows):
        r, n = rows[i]
        i += 1
        while i < len(rows) and rows[i][0] == r:
            n += rows[i][1]
            i += 1
        yield {"key": r[0], "role": r[1], "o": r[2], "x": r[3], "slot": r[4], "n": n}


def _ak_class(slot: Any) -> str:
    """The slot class the store keys asked_tally by: "" for a whole ask, the attribute otherwise
    ("o3.col" -> "col"; L6a's folded key "#col" -> "col")."""
    if slot is None:
        return ""
    return slot[1:] if slot.startswith("#") else slot.split(".", 1)[-1]


def _ak_entries3(ag: Any, tok: Any, sig: tuple) -> Any:
    """L1 FORM 3 (the reviewer 2026-10-20 11:06, 11:13): the asked record in its readers' own form
    -- one tally row per (key, role, slot class) with n (times asked) and v (counter rows), which is
    all asked_tally reads, and one whole row per (key, role, o, x) asked whole ("w"), which is all
    ak_whole (and so recorded_whole) reads. Sorted, so the file is a function of the counter."""
    tally: dict = {}
    whole: dict = {}
    for k, n in ag._ak_asked.items():
        if k[0] != tok or not (k[1] is sig or k[1] == sig):
            continue
        key, role, o, x, slot = k[2:]
        t = tally.setdefault((key, role, _ak_class(slot)), [0, 0])
        t[0] += n
        t[1] += 1
        if slot is None:
            whole[(key, role, o, x)] = whole.get((key, role, o, x), 0) + n
    for (key, role, sc), (n, v) in sorted(tally.items(), key=repr):
        yield {"key": key, "role": role, "sc": sc, "n": n, "v": v}
    for (key, role, o, x), n in sorted(whole.items(), key=repr):
        yield {"key": key, "role": role, "o": o, "x": x, "slot": None, "n": n, "w": 1}


def _put_memo_stream(p: Path, h: str, prefix: str, sig: tuple, entries: Any, extra: dict,
                     chunk: int = 20000) -> dict:
    """_put_memo's file, BYTE-IDENTICAL to _dumps of the same body, written as it is encoded (S5 c,
    the reviewer 09:36): the entries in bounded chunks through a running sha256 into a .part file,
    renamed to its hash name at the end -- a rename never overwrites, as "xb" never does. Every
    other key of the body sorts after "entries", so the entries open the object."""
    arm, parts = _sig_parts(sig)
    rest = {"gen": h, "sig_arm": arm, "sig_atoms": parts, "refused": [], **extra}
    assert all(k > "entries" for k in rest), "the entries must be the body's first key"
    tail = _dumps(rest)
    tmp = p / f"{prefix}{h}.part"
    moved = []
    if tmp.exists():   # a crash's leftover: never a save (no hash name), and never deleted (09:45)
        moved.append(_set_aside(tmp))
    import zlib
    sha, n, first = hashlib.sha256(), 0, True
    z = zlib.compressobj(6) if _COMPRESS else None
    with open(tmp, "xb") as fh:
        def put(b: bytes) -> None:
            sha.update(b)        # the name is the hash of the UNCOMPRESSED bytes (L2)
            fh.write(z.compress(b) if z is not None else b)
        put(b'{"entries":[')
        buf: list = []
        for e in entries:
            buf.append(json.dumps(e, sort_keys=True, separators=(",", ":")))
            n += 1
            if len(buf) >= chunk:
                put(("" if first else ",").encode() + ",".join(buf).encode("utf-8"))
                first, buf = False, []
        if buf:
            put(("" if first else ",").encode() + ",".join(buf).encode("utf-8"))
        put(b"]," + tail[1:])
        if z is not None:
            fh.write(z.flush())
    name = f"{prefix}{h}_{sha.hexdigest()[:16]}.json"
    try:
        os.rename(tmp, p / name)
    except FileExistsError:
        moved.append(_set_aside(tmp))
        return {"refused": f"{name} exists; a memo file is never overwritten", "set_aside": moved}
    return {"written": name, "entries": n, "refused": 0, **({"set_aside": moved} if moved else {})}


def _set_aside(f: Path) -> dict:
    """A file the code made and will not use is RENAMED aside under a tombstone name, never deleted
    (the reviewer 09:45: nothing is deleted without Isaiah's word); the caller records the row."""
    stamp = time.strftime("%Y%m%dT%H%M%SZ", time.gmtime())
    dead = f.with_name(f"{f.name}.dead-{stamp}")
    size = f.stat().st_size
    os.rename(f, dead)
    return {"path": str(dead), "bytes": size, "stamp": stamp}


def write_ak(d: str | Path, ag: Any, h: str) -> dict | None:
    """Beside generation `h`: the questions this signature answered that no ak_ file holds.
    Under TETHER_MEMORY_STORE (S4, the reviewer 08:26 item 3): the questions asked SINCE THE LAST
    SAVE, each with n = times asked, in form 2; the counter is cleared once the file is written."""
    import compile_term
    import tether
    if not (_CARRY and _RECORD and tether._INDEX_HOLD and tether._SLOT_FILTER):
        return None
    p = Path(d)
    sig = compile_term.signature({a.name: a for a in ag.gamma.atoms})
    if _MEMORY_STORE:
        tok = getattr(ag, "_atoms_token", None)
        out = (_put_memo_stream(p, h, AKMEMO, sig, _ak_entries3(ag, tok, sig), {"form": 3})
               if _COMPRESS else
               _put_memo_stream(p, h, AKMEMO, sig, _ak_entries(ag, tok, sig), {"form": 2}))
        for m in out.get("set_aside", ()):
            _c, _s, _lv = ag._boundary_key("@lineage")
            ag.led.record(_c, "SETTLE", _s, "set_aside", **_lv, **m,
                          reads="a .part the code made and did not use, renamed aside, not deleted")
        if "written" in out:
            ag._ak_asked.clear()
        return out
    known = _AK_CARRIED.setdefault(str(p.resolve()), set())
    entries = []
    for (s, key, role, o, x), slot in _ak_source(ag):
        if s != sig or (key, role, o, x, slot) in known:
            continue
        entries.append({"key": key, "role": role, "o": o, "x": x, "slot": slot})
    out = _put_memo(p, h, AKMEMO, sig, entries, [])
    if "written" in out:
        known.update((e["key"], e["role"], e["o"], e["x"], e["slot"]) for e in entries)
    return out


def load_ak(d: str | Path, ag: Any, chain: list) -> dict | None:
    """Each generation's ak_ files, root to tip, PENDING their first ask (recorded). A file of
    ANOTHER signature still loads (R1, the reviewer 2026-10-15 13:47; Isaiah 13:26 "the record is
    never dropped"): it is counted as signature_differs and its questions pend under the current
    signature, where the answer is rebuilt from the current, live-checked held view."""
    import compile_term
    import tether
    if not (_CARRY and _RECORD and tether._INDEX_HOLD and tether._SLOT_FILTER) or not chain:
        return None
    p = Path(d)
    sig = compile_term.signature({a.name: a for a in ag.gamma.atoms})
    folder = str(p.resolve())
    known = _AK_CARRIED.setdefault(folder, set())
    rep: dict = {"pending": 0, "absent": 0, "signature_differs": 0, "unreadable": 0, "bytes": 0}
    for gh, body in _memo_bodies(p, AKMEMO, sig, chain, rep, any_sig=True):
        for e in body["entries"]:
            if "sc" in e:      # a form-3 tally row: no instance, no pending question (L1)
                continue
            k = (sig, e["key"], e["role"], e["o"], e["x"])
            _AK_PENDING.setdefault(k, {"gen": gh, "slots": set(), "folder": folder})["slots"].add(
                e["slot"])
            known.add((e["key"], e["role"], e["o"], e["x"], e["slot"]))
    rep["pending"] = len(_AK_PENDING)
    return rep


def recorded_whole(mkey: tuple) -> bool:
    """At a pair's first ask: was it recorded as a WHOLE (reused) in an earlier process? The record
    is consumed here; a pair recorded only for slots is counted and takes the first-slot path."""
    _tok, sig, key, role, o, x = mkey
    p = _AK_PENDING.pop((sig, key, role, o, x), None)
    if p is None:
        return False
    if None in p["slots"]:
        _AK_N["whole"] += 1
        return True
    _AK_N["slot"] += 1
    return False
