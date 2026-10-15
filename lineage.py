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
standing or into a live store (standing is 7i's; the kind forms are (b'-l) phase 2's)."""
from __future__ import annotations

import dataclasses
import hashlib
import heapq
import json
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


def _dumps(x: Any) -> bytes:
    """The one form every lineage file is written in (S1f, the reviewer 2026-10-15 13:01): sorted
    keys and compact separators (indent=1 was 42% of the bytes, the 12:59 read). Every file is
    checked against the hash of its own bytes, so a file written indented still loads and
    verifies; a new file's name differs because its bytes do, its content is the same."""
    return json.dumps(x, sort_keys=True, separators=(",", ":")).encode("utf-8")


def _read(d: Path) -> dict[str, dict]:
    """Every generation in `d`, each verified against its own name; raises on a bad hash or a
    parent that is not in the folder."""
    gens: dict[str, dict] = {}
    for f in sorted(d.glob(f"{PREFIX}*.json")):
        raw = f.read_bytes()
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


def write(d: str | Path, ag: Any, game: str) -> dict:
    """The boundary's generation: only what changed since the parent the instance LOADED
    (ag.lineage_parent), against that parent's fold. Named by its own hash; never overwritten."""
    p = Path(d)
    p.mkdir(parents=True, exist_ok=True)
    parent = getattr(ag, "lineage_parent", None)
    chain = _chain(p)
    # the parent and what it descends from, in fold order (a DAG has no prefix to slice)
    keep = _ancestors(dict(chain), parent) if parent else set()
    upto = [(h, g) for h, g in chain if h in keep]
    base = fold(upto)
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
           "vindication_tail": list(blob["vindication"])[len(base["vindication"]):],
           "book": {k: v for k, v in blob["book"].items() if base["book"].get(k) != v},
           "invented": {n: r for n, r in blob["invented"].items() if n not in base["invented"]},
           "dormant": dormant, "dormant_refused": refused}
    raw = _dumps(gen)
    h = hashlib.sha256(raw).hexdigest()[:16]
    try:
        with open(p / f"{PREFIX}{h}.json", "xb") as fh:
            fh.write(raw)
    except FileExistsError:
        return {"refused": f"{PREFIX}{h}.json exists; a generation is never overwritten"}
    if _BOUNDARY:   # the next write in this instance extends THIS one: one line (F2)
        ag.lineage_parent = h
        ag._lineage_written = {**written, **{n: {"born": h, "handle": hd} for n, hd in new_names}}
        ag._lineage_marks = {"dormant": len(dormant_all), "evidence": len(ag.gamma.evidence)}
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
    return {"written": f"{PREFIX}{h}.json", "hash": h, "parent": parent, "terms": len(terms),
            "status": len(status), "evidence": len(gen["evidence"]), "dormant": len(dormant),
            "dormant_refused": len(refused), "index": idx, "memo": memo,
            "slot_memo": slot_memo}


def boundary(d: str | Path | None, ag: Any, game: str, how: str) -> dict | None:
    """THE BOUNDARY WRITE, one path for both runners (arc_holdout.play, tether_agent.run): a
    generation at a level clear ("level") or a terminal edge ("death", "game_win"), as write() makes
    one at the game's end. None unless the boundary arm, the carry and a folder are all present."""
    if not (_BOUNDARY and _CARRY and d):
        return None
    # agent_level: Agent.level, which counts WIN/death edges, and level clears too only under
    # TETHER_LEVEL_EDGE (F1); the 'how' field is the true label of the write
    return {"how": how, "agent_level": ag.level, **write(d, ag, game)}


def load(d: str | Path, ag: Any) -> dict:
    """The next instance's start: the chain folded into its Gamma as IMPORTED terms naming the tip,
    and the evidence record turned on. The fold's evidence and dormant record are not read back."""
    h, f = head(d)
    ag.lineage_parent = h
    ag.gamma.keep_evidence = True
    if h is None:
        return {"parent": None, "root": "no generation yet; this instance writes the first"}
    rep = ag.gamma.load_blob({"terms": f["terms"], "invented": f["invented"],
                              "vindication": f["vindication"], "book": f["book"]}, parent=h)
    chain = _chain(Path(d))
    return {"parent": h, **rep, "index": load_index(d, ag, chain),
            "memo": load_memo(d, ag, chain), "slot_memo": load_bs(d, ag, chain)}


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
            fh.write(raw)
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
                "parties": list(c.parties), "absent": enc(c.absent)}
    raise Unencodable(type(c).__name__)


def _dec_c(x: Any, atoms: dict) -> Any:
    import compile_term
    if x is None:
        return None
    if "refusal" in x:
        return compile_term.Refusal(x["refusal"])
    return compile_term.Compiled(x["slot"], _dec_term(x["term"], atoms), x["operand"],
                                 tuple(x["parties"]), dec(x["absent"]))


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
            fh.write(raw)
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
            raw = files[0].read_bytes()
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
            fh.write(raw)
    except FileExistsError:
        return {"refused": f"{name} exists; a memo file is never overwritten"}
    return {"written": name, "entries": len(entries), "refused": len(refused)}


def _memo_bodies(p: Path, prefix: str, sig: tuple, chain: list, rep: dict) -> Any:
    """Each generation's memo files of one family, root to tip: the body of every file whose name
    is its own hash and whose signature is EQUAL; every other file is counted, never read on."""
    arm, parts = _sig_parts(sig)
    for gh, _g in chain:
        if _g.get("merge"):
            continue
        files = sorted(p.glob(f"{prefix}{gh}_*.json"))
        if not files:
            rep["absent"] += 1      # a generation written before the memo carried, or with none
            continue
        for f in files:
            raw = f.read_bytes()
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
                continue
            yield gh, body


def write_memo(d: str | Path, ag: Any, h: str) -> dict | None:
    """Beside generation `h`: the bound answers for this Gamma's signature that no memo file of
    this chain already holds (the extension, never a copy). Opened "xb", named by its own hash."""
    import compile_term
    import tether
    if not (_CARRY and tether._INDEX_HOLD):
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
        kept = [i for i, (_c, a, b) in enumerate(held) if tether._lands(role, a, b, slot, sub)]
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
