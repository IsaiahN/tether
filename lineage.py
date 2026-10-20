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
import json
from pathlib import Path
from typing import Any

import armflag
import gamma
import sensors

CARRY = armflag.arm("TETHER_LINEAGE_CARRY")
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


def _chain(d: Path) -> list[tuple[str, dict]]:
    """Every generation in `d`, root to tip, each verified against its own name. Raises on a bad
    hash, a missing parent, more than one root or more than one tip (N3)."""
    gens: dict[str, dict] = {}
    for f in sorted(d.glob(f"{PREFIX}*.json")):
        raw = f.read_bytes()
        h = hashlib.sha256(raw).hexdigest()[:16]
        if f.stem != PREFIX + h:
            raise ValueError(f"lineage: {f.name} does not hash to its name ({h})")
        gens[h] = json.loads(raw)
    if not gens:
        return []
    parents = {h: g["parent"] for h, g in gens.items()}
    bad = {h: p for h, p in parents.items() if p is not None and p not in gens}
    if bad:
        raise ValueError(f"lineage: a parent that is not in the chain: {bad}")
    roots = [h for h, p in parents.items() if p is None]
    tips = sorted(set(gens) - {p for p in parents.values() if p is not None})
    if len(roots) != 1 or len(tips) != 1:
        raise ValueError(f"lineage: not one chain (roots {sorted(roots)}, tips {tips}); merging "
                         "branches is not this item's")
    order, h = [], tips[0]
    while h is not None:
        order.append((h, gens[h]))
        h = parents[h]
    if len(order) != len(gens):
        raise ValueError(f"lineage: {len(gens) - len(order)} generation(s) off the chain")
    return order[::-1]


def fold(chain: list[tuple[str, dict]]) -> dict:
    """The chain read as one library, root to tip. Every row is kept, each stamped with the
    generation it was first written in ("born"); nothing is removed (N2)."""
    rows: dict[tuple, dict] = {}
    out = {"terms": [], "invented": {}, "vindication": [], "book": {}, "evidence": [],
           "dormant": []}
    for h, g in chain:
        for r in g["terms"]:
            row = {**r, "born": h}
            rows[_rid(row)] = row
        for s in g["status"]:
            rows[(s["born"], s["handle"])]["admitted"] = s["admitted"]
        out["invented"].update(g["invented"])
        out["vindication"].extend(g["vindication_tail"])
        out["book"].update(g["book"])
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
    upto = chain[:[h for h, _ in chain].index(parent) + 1] if parent else []
    base = fold(upto)
    prev = {_rid(r): r for r in base["terms"]}
    blob = ag.gamma.blob(with_names=True)
    terms, status = [], []
    for r in blob["terms"]:
        # NEW = minted by this instance; a term it LOADED from the lineage carries its identity
        # in carried (born, handle), and only a non-marker change of its status is written (N1).
        c = ag.gamma.carried.get(r.pop("name")) or {}
        rid = (c.get("born"), c.get("handle"))
        if rid not in prev:
            terms.append(r)
        elif r.get("admitted") not in (None, gamma.IMPORTED, prev[rid].get("admitted")):
            status.append({"born": rid[0], "handle": rid[1], "admitted": r["admitted"]})
    # THE DORMANT RECORD ITEM BY ITEM (the reviewer 21:14, I3): an item enc has no form for is
    # not written, and is named; it never costs the generation its terms, status or evidence.
    dormant, refused = [], []
    for i, item in enumerate(getattr(ag, "_dormant", [])):
        try:
            dormant.append(enc(item))
        except Unencodable as e:
            refused.append({"i": i, "type": e.type})
    gen = {"lineage": 1, "parent": parent, "game": game, "terms": terms, "status": status,
           "evidence": list(ag.gamma.evidence),
           "vindication_tail": list(blob["vindication"])[len(base["vindication"]):],
           "book": {k: v for k, v in blob["book"].items() if base["book"].get(k) != v},
           "invented": {n: r for n, r in blob["invented"].items() if n not in base["invented"]},
           "dormant": dormant, "dormant_refused": refused}
    raw = json.dumps(gen, sort_keys=True, indent=1).encode("utf-8")
    h = hashlib.sha256(raw).hexdigest()[:16]
    try:
        with open(p / f"{PREFIX}{h}.json", "xb") as fh:
            fh.write(raw)
    except FileExistsError:
        return {"refused": f"{PREFIX}{h}.json exists; a generation is never overwritten"}
    # D3: the index AFTER the generation; its failure is recorded and never costs the generation
    try:
        idx = write_index(p, ag, h)
    except Exception as e:  # noqa: BLE001 -- recorded in the report, never raised past here
        idx = {"failed": f"{type(e).__name__}: {e}"[:200]}
    return {"written": f"{PREFIX}{h}.json", "hash": h, "parent": parent, "terms": len(terms),
            "status": len(status), "evidence": len(gen["evidence"]), "dormant": len(dormant),
            "dormant_refused": len(refused), "index": idx}


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
    return {"parent": h, **rep, "index": load_index(d, ag, _chain(Path(d)))}


# -- D3: THE HELD INDEX, CARRIED BESIDE THE GENERATION (the reviewer 2026-10-14 21:59) -------------
# Under BOTH arms (CARRY and tether's INDEX_HOLD), each generation gets an index file beside it
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
                            "items": [{"i": i, "ch": _ch(cand), "c": _enc_c(c), "t": _enc_c(t)}
                                      for i, (cand, c, t) in enumerate(held)]})
        except Unencodable as e:
            refused.append({"key": key, "role": role, "type": e.type})
    arm, parts = _sig_parts(sig)
    raw = json.dumps({"gen": h, "sig_arm": arm, "sig_atoms": parts,
                      "sig_names": sorted(a[0] for a in sig[1]), "entries": entries,
                      "refused": refused}, sort_keys=True, indent=1).encode("utf-8")
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
    for gh, _g in chain:
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
            if not same and any(isinstance(z, compile_term.Refusal)
                                for _, _, b, c in items for z in (b, c)):
                rep["refusals_recompile"] += 1
                continue
            k = (sig, e["key"], e["role"])
            if k not in tether._INDEX_STORE and k not in _PENDING:
                _PENDING[k] = {"gen": gh, "items": items}
                rep["installed" if same else "rekeyed"] += 1
            known.add((repr(sig), e["key"], e["role"]))
    return rep


def resolve(ag: Any, lib: Any, key: str, role: str, sig: tuple) -> list | None:
    """A carried reference at its FIRST ask (tether._held_index, both arms): the library's own view
    under the placeholders, checked WHOLE -- the same length and every position's hash. All match:
    the carried compiles are held and nothing is compiled. Any miss: the entry is dropped for this
    instance and compiled fresh, counted, and its generation writes one index_rebuild row."""
    import tether
    p = _PENDING.pop((sig, key, role), None)
    if p is None:
        return None
    view = lib.view(key, role, tether.PH_O, tether.PH_X)
    items = p["items"]
    if len(view) == len(items) and all(i < len(view) and _ch(view[i]) == ch
                                       for i, ch, _, _ in items):
        held = [(view[i], c, t) for i, _, c, t in items]
        tether._INDEX_STORE[(sig, key, role)] = held
        _RESOLVE["resolved"] += 1
        return held
    _RESOLVE["unresolved"] += 1
    if p["gen"] not in _ROWED:
        _ROWED.add(p["gen"])
        _c, _s, _lv = ag._boundary_key("@lineage")
        ag.led.record(_c, "IMPORT", _s, "index_rebuild", **_lv, generation=p["gen"],
                      reason="unresolved candidates: the library's view no longer matches",
                      reads="the entry compiled fresh; the carried compile was not used")
    return None
